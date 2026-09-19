const API_URL = "http://127.0.0.1:8000";


// ==========================================
// DEFAULT PROCEDURE COSTS
// ==========================================

const procedureCosts = {
    "D1110": 100,
    "D0210": 150,
    "D0274": 120,
    "D2391": 200,
    "D2740": 800,
    "D2750": 800,
    "D3310": 900,
    "D7140": 250,
    "D9999": 500
};


// ==========================================
// DOM ELEMENTS
// ==========================================

const demoPatient = document.getElementById("demoPatient");
const memberIdInput = document.getElementById("memberId");
const procedureList = document.getElementById("procedureList");
const verifyButton = document.getElementById("verifyButton");
const result = document.getElementById("result");
const reportActions = document.getElementById("reportActions");
const historyContainer = document.getElementById("historyContainer");
const clearHistoryButton = document.getElementById("clearHistoryButton");


// ==========================================
// CURRENT VERIFICATION DATA
// ==========================================

let currentVerificationData = null;


// ==========================================
// DEMO PATIENT SELECTION
// ==========================================

demoPatient.addEventListener("change", function () {

    const selectedMemberId = demoPatient.value;

    if (!selectedMemberId) {

        memberIdInput.value = "";

        procedureList.innerHTML = `
            <div class="procedure-placeholder">
                Select a patient first to load available procedures.
            </div>
        `;

        result.innerHTML = "";
        reportActions.innerHTML = "";

        return;
    }

    memberIdInput.value = selectedMemberId;

    loadPatient(selectedMemberId);
});


// ==========================================
// MEMBER ID LOOKUP
// ==========================================

memberIdInput.addEventListener("blur", function () {

    const memberId = memberIdInput.value.trim();

    if (!memberId) {
        return;
    }

    loadPatient(memberId);
});


// ==========================================
// LOAD PATIENT
// ==========================================

async function loadPatient(memberId) {

    result.innerHTML = "";
    reportActions.innerHTML = "";

    procedureList.innerHTML = `
        <div class="procedure-placeholder">
            Loading patient information...
        </div>
    `;


    try {

        const response = await fetch(
            `${API_URL}/patient/${memberId}/info`
        );


        if (!response.ok) {

            const errorData = await response.json();

            throw new Error(
                errorData.detail || "Patient not found."
            );
        }


        const patientData = await response.json();

        displayPatientInformation(patientData);

        await loadPatientProcedures(memberId);

    } catch (error) {

        procedureList.innerHTML = `
            <div class="patient-lookup-error">
                ${escapeHtml(error.message)}
            </div>
        `;
    }
}


// ==========================================
// DISPLAY PATIENT INFORMATION
// ==========================================

function displayPatientInformation(data) {

    let statusClass = "lookup-status-info";


    if (data.policy_status === "Active") {

        statusClass = "lookup-status-active";

    } else if (
        data.policy_status === "Expired"
        ||
        data.policy_status === "Cancelled"
    ) {

        statusClass = "lookup-status-inactive";
    }


    result.innerHTML = `

        <div class="card patient-lookup-card">

            <div class="patient-lookup-header">

                <div>

                    <strong>
                        ${escapeHtml(data.name)}
                    </strong>

                    <span>
                        Patient Information
                    </span>

                </div>


                <span class="lookup-status ${statusClass}">

                    ${escapeHtml(data.policy_status)}

                </span>

            </div>


            <div class="patient-lookup-details">

                <div>

                    <small>
                        Patient Name
                    </small>

                    <strong>
                        ${escapeHtml(data.name)}
                    </strong>

                </div>


                <div>

                    <small>
                        Date of Birth
                    </small>

                    <strong>
                        ${escapeHtml(data.dob)}
                    </strong>

                </div>


                <div>

                    <small>
                        Member ID
                    </small>

                    <strong>
                        ${escapeHtml(data.member_id)}
                    </strong>

                </div>


                <div>

                    <small>
                        Insurance Provider
                    </small>

                    <strong>
                        ${escapeHtml(data.provider)}
                    </strong>

                </div>


                <div>

                    <small>
                        Insurance Status
                    </small>

                    <strong>
                        ${escapeHtml(data.policy_status)}
                    </strong>

                </div>

            </div>

        </div>

    `;
}


// ==========================================
// LOAD PATIENT PROCEDURES
// ==========================================

async function loadPatientProcedures(memberId) {

    try {

        const response = await fetch(
            `${API_URL}/patient/${memberId}/procedures`
        );


        if (!response.ok) {

            const errorData = await response.json();

            throw new Error(
                errorData.detail ||
                "Unable to load procedures."
            );
        }


        const data = await response.json();

        displayProcedures(data.procedures);

    } catch (error) {

        procedureList.innerHTML = `
            <div class="patient-lookup-error">
                ${escapeHtml(error.message)}
            </div>
        `;
    }
}


// ==========================================
// DISPLAY AVAILABLE PROCEDURES
// ==========================================

function displayProcedures(procedures) {

    if (!procedures || procedures.length === 0) {

        procedureList.innerHTML = `
            <div class="procedure-placeholder">
                No procedures available for this patient.
            </div>
        `;

        return;
    }


    procedureList.innerHTML = "";


    procedures.forEach(function (procedure) {

        const defaultCost =
            procedureCosts[procedure.procedure_code] || 0;


        const procedureItem =
            document.createElement("div");


        procedureItem.className =
            "procedure-item";


        procedureItem.innerHTML = `

            <div class="procedure-selection">

                <label>

                    <input
                        type="checkbox"
                        class="procedure-checkbox"
                        value="${escapeHtml(
                            procedure.procedure_code
                        )}"
                    >

                    <span>

                        <strong>
                            ${escapeHtml(
                                procedure.procedure_code
                            )}
                        </strong>

                        -
                        ${escapeHtml(
                            procedure.procedure_name
                        )}

                    </span>

                </label>

            </div>


            <div class="procedure-cost">

                <label>
                    Procedure Cost
                </label>

                <input
                    type="number"
                    class="procedure-cost-input"
                    value="${defaultCost}"
                    min="0"
                    step="0.01"
                    disabled
                >

            </div>

        `;


        procedureList.appendChild(
            procedureItem
        );
    });


    setupProcedureCheckboxes();
}


// ==========================================
// PROCEDURE CHECKBOXES
// ==========================================

function setupProcedureCheckboxes() {

    const checkboxes =
        document.querySelectorAll(
            ".procedure-checkbox"
        );


    checkboxes.forEach(function (checkbox) {

        checkbox.addEventListener(
            "change",
            function () {

                const procedureItem =
                    checkbox.closest(
                        ".procedure-item"
                    );


                const costInput =
                    procedureItem.querySelector(
                        ".procedure-cost-input"
                    );


                costInput.disabled =
                    !checkbox.checked;


                if (checkbox.checked) {

                    costInput.focus();
                }
            }
        );
    });
}


// ==========================================
// VERIFY INSURANCE
// ==========================================

verifyButton.addEventListener(
    "click",
    async function () {

        const memberId =
            memberIdInput.value.trim();


        if (!memberId) {

            showError(
                "Please enter or select a Member ID."
            );

            return;
        }


        const selectedProcedures = [];


        const procedureItems =
            document.querySelectorAll(
                ".procedure-item"
            );


        let invalidCost = false;


        procedureItems.forEach(function (item) {

            const checkbox =
                item.querySelector(
                    ".procedure-checkbox"
                );


            const costInput =
                item.querySelector(
                    ".procedure-cost-input"
                );


            if (checkbox && checkbox.checked) {

                const procedureCode =
                    checkbox.value;


                const procedureCost =
                    parseFloat(
                        costInput.value
                    );


                if (
                    Number.isNaN(procedureCost)
                    ||
                    procedureCost < 0
                ) {

                    invalidCost = true;

                    return;
                }


                selectedProcedures.push({

                    procedure_code:
                        procedureCode,

                    procedure_cost:
                        procedureCost

                });
            }
        });


        if (invalidCost) {

            showError(
                "Please enter a valid cost for every selected procedure."
            );

            return;
        }


        if (selectedProcedures.length === 0) {

            showError(
                "Please select at least one procedure."
            );

            return;
        }


        verifyButton.disabled = true;

        verifyButton.textContent =
            "Verifying Insurance...";


        result.innerHTML = `

            <div class="patient-lookup-loading">

                Verifying insurance coverage...

            </div>

        `;


        reportActions.innerHTML = "";


        try {

            const response = await fetch(
                `${API_URL}/patient/${memberId}/verify-multiple`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        procedures:
                            selectedProcedures

                    })
                }
            );


            if (!response.ok) {

                const errorData =
                    await response.json();


                throw new Error(
                    errorData.detail ||
                    "Verification failed."
                );
            }


            const data =
                await response.json();


            currentVerificationData =
                data;


            displayVerificationResult(
                data
            );


            saveVerificationHistory(
                data
            );


            displayHistory();

        } catch (error) {

            showError(
                error.message
            );

        } finally {

            verifyButton.disabled = false;

            verifyButton.textContent =
                "Verify Insurance";
        }
    }
);


// ==========================================
// DISPLAY VERIFICATION RESULT
// ==========================================

function displayVerificationResult(data) {

    const patient = data.patient;
    const policy = data.policy;
    const verification = data.verification;


    let statusClass =
        "not-eligible";


    let statusIcon =
        "✕";


    if (
        verification.overall_status ===
        "ELIGIBLE"
    ) {

        statusClass =
            "eligible";

        statusIcon =
            "✓";

    } else if (
        verification.overall_status ===
        "NEEDS REVIEW"
    ) {

        statusClass =
            "review";

        statusIcon =
            "!";
    }


    result.innerHTML = `

        <div class="result-container">


            <!-- =========================
                 PATIENT INFORMATION
            ========================== -->

            <div class="card result-card">

                <h2>
                    Patient Information
                </h2>


                <div class="info-grid">

                    <div class="info-item">

                        <strong>
                            Patient Name
                        </strong>

                        <span>
                            ${escapeHtml(
                                patient.name
                            )}
                        </span>

                    </div>


                    <div class="info-item">

                        <strong>
                            Date of Birth
                        </strong>

                        <span>
                            ${escapeHtml(
                                patient.dob
                            )}
                        </span>

                    </div>


                    <div class="info-item">

                        <strong>
                            Member ID
                        </strong>

                        <span>
                            ${escapeHtml(
                                patient.member_id
                            )}
                        </span>

                    </div>


                    <div class="info-item">

                        <strong>
                            Insurance Provider
                        </strong>

                        <span>
                            ${escapeHtml(
                                patient.provider
                            )}
                        </span>

                    </div>


                    <div class="info-item">

                        <strong>
                            Policy Status
                        </strong>

                        <span>
                            ${escapeHtml(
                                policy.status
                            )}
                        </span>

                    </div>


                    <div class="info-item">

                        <strong>
                            Policy Period
                        </strong>

                        <span>
                            ${escapeHtml(
                                policy.start_date
                            )}

                            to

                            ${escapeHtml(
                                policy.end_date
                            )}
                        </span>

                    </div>


                    <div class="info-item">

                        <strong>
                            Annual Limit
                        </strong>

                        <span>
                            $${formatMoney(
                                policy.annual_limit
                            )}
                        </span>

                    </div>


                    <div class="info-item">

                        <strong>
                            Remaining Limit
                        </strong>

                        <span>
                            $${formatMoney(
                                policy.remaining_limit
                            )}
                        </span>

                    </div>


                    <div class="info-item">

                        <strong>
                            Deductible
                        </strong>

                        <span>
                            $${formatMoney(
                                policy.deductible
                            )}
                        </span>

                    </div>


                    <div class="info-item">

                        <strong>
                            Remaining Deductible
                        </strong>

                        <span>
                            $${formatMoney(
                                policy.deductible_remaining
                            )}
                        </span>

                    </div>

                </div>

            </div>


            <!-- =========================
                 OVERALL STATUS
            ========================== -->

            <div class="overall-status ${statusClass}">

                <div class="overall-icon">

                    ${statusIcon}

                </div>


                <div class="overall-content">

                    <small>
                        INSURANCE VERIFICATION
                    </small>

                    <h2>
                        ${escapeHtml(
                            verification.overall_status
                        )}
                    </h2>

                    <p>
                        ${getOverallMessage(
                            verification.overall_status
                        )}
                    </p>

                </div>

            </div>


            <!-- =========================
                 VERIFICATION SUMMARY
            ========================== -->

            <div class="card">

                <h2>
                    Verification Summary
                </h2>


                <div class="verification-summary">

                    <div class="summary-item summary-total">

                        <strong>
                            ${verification.procedure_count}
                        </strong>

                        <span>
                            Procedures
                        </span>

                    </div>


                    <div class="summary-item summary-total">

                        <strong>
                            $${formatMoney(
                                verification.total_procedure_cost
                            )}
                        </strong>

                        <span>
                            Total Cost
                        </span>

                    </div>


                    <div class="summary-item summary-pass">

                        <strong>
                            $${formatMoney(
                                verification.total_estimated_insurance_payment
                            )}
                        </strong>

                        <span>
                            Insurance Estimate
                        </span>

                    </div>


                    <div class="summary-item summary-review">

                        <strong>
                            $${formatMoney(
                                verification.total_estimated_patient_responsibility
                            )}
                        </strong>

                        <span>
                            Patient Responsibility
                        </span>

                    </div>

                </div>

            </div>


            <!-- =========================
                 PROCEDURE DETAILS
            ========================== -->

            <div class="card">

                <h2>
                    Procedure Details
                </h2>


                <div class="procedure-results">

                    ${verification.procedures
                        .map(function (procedure) {

                            return createProcedureResult(
                                procedure
                            );

                        })
                        .join("")}

                </div>

            </div>


            <!-- =========================
                 POLICY DETAILS
            ========================== -->

            <div class="card">

                <h2>
                    Policy Details
                </h2>


                <div class="info-grid">

                    <div class="info-item">

                        <strong>
                            Annual Maximum
                        </strong>

                        <span>
                            $${formatMoney(
                                policy.annual_limit
                            )}
                        </span>

                    </div>


                    <div class="info-item">

                        <strong>
                            Remaining Maximum
                        </strong>

                        <span>
                            $${formatMoney(
                                policy.remaining_limit
                            )}
                        </span>

                    </div>


                    <div class="info-item">

                        <strong>
                            Deductible
                        </strong>

                        <span>
                            $${formatMoney(
                                policy.deductible
                            )}
                        </span>

                    </div>


                    <div class="info-item">

                        <strong>
                            Remaining Deductible
                        </strong>

                        <span>
                            $${formatMoney(
                                policy.deductible_remaining
                            )}
                        </span>

                    </div>

                </div>

            </div>

        </div>

    `;


    createReportButton();
}


// ==========================================
// CREATE PROCEDURE RESULT
// ==========================================

function createProcedureResult(procedure) {

    const coveragePercentage =
        Number(
            procedure.coverage_percentage
        );


    const coveragePass =
        procedure.coverage_status ===
        "PASS";


    const frequencyPass =
        procedure.frequency_status ===
        "PASS";


    const coverageClass =
        coveragePass
            ? "check-pass"
            : "check-fail";


    const frequencyClass =
        frequencyPass
            ? "check-pass"
            : "check-fail";


    const coverageIcon =
        coveragePass
            ? "✓"
            : "✕";


    const frequencyIcon =
        frequencyPass
            ? "✓"
            : "✕";


    return `

        <div class="procedure-result">


            <div>

                <strong>
                    ${escapeHtml(
                        procedure.procedure_code
                    )}
                </strong>

                <span>
                    ${escapeHtml(
                        procedure.procedure_name
                    )}
                </span>

            </div>


            <div>

                <p>
                    <strong>
                        Coverage
                    </strong>
                </p>

                <p>
                    ${coveragePercentage.toFixed(0)}%
                </p>


                <div class="progress-bar">

                    <div
                        class="progress-fill"
                        style="width: ${coveragePercentage}%"
                    ></div>

                </div>

            </div>


            <div>

                <p>

                    <strong>
                        Procedure Cost
                    </strong>

                    $${formatMoney(
                        procedure.procedure_cost
                    )}

                </p>


                <p>

                    <strong>
                        Deductible Applied
                    </strong>

                    $${formatMoney(
                        procedure.deductible_applied
                    )}

                </p>

            </div>


            <div class="${coverageClass} check">

                <div class="check-icon">

                    ${coverageIcon}

                </div>


                <div class="check-content">

                    <strong>
                        Coverage
                    </strong>

                    <span class="status">

                        ${escapeHtml(
                            procedure.coverage_status
                        )}

                    </span>

                    <p>

                        ${escapeHtml(
                            procedure.coverage_message
                        )}

                    </p>

                </div>

            </div>


            <div class="${frequencyClass} check">

                <div class="check-icon">

                    ${frequencyIcon}

                </div>


                <div class="check-content">

                    <strong>
                        Frequency Limit
                    </strong>

                    <span class="status">

                        ${escapeHtml(
                            procedure.frequency_status
                        )}

                    </span>

                    <p>

                        ${escapeHtml(
                            procedure.frequency_message
                        )}

                    </p>

                </div>

            </div>


            <div class="cost-estimate">

                <h3>
                    Cost Estimate
                </h3>


                <div class="cost-row">

                    <span>
                        Procedure Cost
                    </span>

                    <strong>
                        $${formatMoney(
                            procedure.procedure_cost
                        )}
                    </strong>

                </div>


                <div class="cost-row">

                    <span>
                        Deductible Applied
                    </span>

                    <strong>
                        $${formatMoney(
                            procedure.deductible_applied
                        )}
                    </strong>

                </div>


                <div class="cost-row">

                    <span>
                        Coverage
                    </span>

                    <strong>
                        ${coveragePercentage.toFixed(0)}%
                    </strong>

                </div>


                <div class="cost-row">

                    <span>
                        Estimated Insurance Payment
                    </span>

                    <strong>
                        $${formatMoney(
                            procedure.estimated_insurance_payment
                        )}
                    </strong>

                </div>


                <div class="cost-row cost-total">

                    <span>
                        Estimated Patient Responsibility
                    </span>

                    <strong>
                        $${formatMoney(
                            procedure.estimated_patient_responsibility
                        )}
                    </strong>

                </div>

            </div>

        </div>

    `;
}


// ==========================================
// OVERALL STATUS MESSAGE
// ==========================================

function getOverallMessage(status) {

    if (status === "ELIGIBLE") {

        return "The selected procedures meet the available insurance verification checks.";
    }


    if (status === "NEEDS REVIEW") {

        return "Some insurance information requires manual review before proceeding.";
    }


    return "One or more verification checks failed for the selected procedures.";
}


// ==========================================
// REPORT BUTTON
// ==========================================

function createReportButton() {

    reportActions.innerHTML = `

        <button
            class="print-report-button"
            id="printReportButton"
        >
            Print Verification Report
        </button>

    `;


    const printButton =
        document.getElementById(
            "printReportButton"
        );


    printButton.addEventListener(
        "click",
        printVerificationReport
    );
}


// ==========================================
// PRINT VERIFICATION REPORT
// ==========================================

function printVerificationReport() {

    if (!currentVerificationData) {
        return;
    }


    const data =
        currentVerificationData;


    const patient =
        data.patient;


    const policy =
        data.policy;


    const verification =
        data.verification;


    const procedureRows =
        verification.procedures
            .map(function (procedure) {

                return `

                    <tr>

                        <td>
                            ${escapeHtml(
                                procedure.procedure_code
                            )}
                        </td>

                        <td>
                            ${escapeHtml(
                                procedure.procedure_name
                            )}
                        </td>

                        <td>
                            $${formatMoney(
                                procedure.procedure_cost
                            )}
                        </td>

                        <td>
                            ${Number(
                                procedure.coverage_percentage
                            ).toFixed(0)}%
                        </td>

                        <td>
                            $${formatMoney(
                                procedure.estimated_insurance_payment
                            )}
                        </td>

                        <td>
                            $${formatMoney(
                                procedure.estimated_patient_responsibility
                            )}
                        </td>

                    </tr>

                `;

            })
            .join("");


    const reportWindow =
        window.open(
            "",
            "_blank"
        );


    reportWindow.document.write(`

        <!DOCTYPE html>

        <html>

        <head>

            <title>
                DenSure Insurance Report
            </title>


            <style>

                body {
                    font-family: Arial, sans-serif;
                    padding: 40px;
                    color: #1f2937;
                }


                h1 {
                    color: #172554;
                    margin-bottom: 5px;
                }


                h2 {
                    color: #172554;
                    margin-top: 30px;
                }


                .subtitle {
                    color: #64748b;
                    margin-bottom: 30px;
                }


                .status {
                    padding: 15px;
                    border-radius: 8px;
                    font-weight: bold;
                    margin: 20px 0;
                }


                .eligible {
                    background: #dcfce7;
                    color: #166534;
                }


                .not-eligible {
                    background: #fee2e2;
                    color: #991b1b;
                }


                .review {
                    background: #fef3c7;
                    color: #92400e;
                }


                .info-grid {
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 10px;
                }


                .info-item {
                    padding: 10px;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                }


                .info-item strong {
                    display: block;
                    margin-bottom: 5px;
                }


                table {
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 15px;
                }


                th,
                td {
                    border: 1px solid #ddd;
                    padding: 10px;
                    text-align: left;
                }


                th {
                    background: #f1f5f9;
                }


                .totals {
                    margin-top: 25px;
                    padding: 20px;
                    background: #f8fafc;
                    border-radius: 8px;
                }


                .total-row {
                    display: flex;
                    justify-content: space-between;
                    padding: 8px 0;
                }

            </style>

        </head>


        <body>


            <h1>
                DenSure
            </h1>


            <div class="subtitle">
                Dental Insurance Verification Report
            </div>


            <div class="status ${getReportStatusClass(
                verification.overall_status
            )}">

                Verification Status:
                ${escapeHtml(
                    verification.overall_status
                )}

            </div>


            <h2>
                Patient Information
            </h2>


            <div class="info-grid">

                <div class="info-item">

                    <strong>
                        Patient Name
                    </strong>

                    ${escapeHtml(
                        patient.name
                    )}

                </div>


                <div class="info-item">

                    <strong>
                        Date of Birth
                    </strong>

                    ${escapeHtml(
                        patient.dob
                    )}

                </div>


                <div class="info-item">

                    <strong>
                        Member ID
                    </strong>

                    ${escapeHtml(
                        patient.member_id
                    )}

                </div>


                <div class="info-item">

                    <strong>
                        Provider
                    </strong>

                    ${escapeHtml(
                        patient.provider
                    )}

                </div>


                <div class="info-item">

                    <strong>
                        Policy Status
                    </strong>

                    ${escapeHtml(
                        policy.status
                    )}

                </div>


                <div class="info-item">

                    <strong>
                        Policy Period
                    </strong>

                    ${escapeHtml(
                        policy.start_date
                    )}

                    to

                    ${escapeHtml(
                        policy.end_date
                    )}

                </div>

            </div>


            <h2>
                Procedure Details
            </h2>


            <table>

                <thead>

                    <tr>

                        <th>
                            Code
                        </th>

                        <th>
                            Procedure
                        </th>

                        <th>
                            Cost
                        </th>

                        <th>
                            Coverage
                        </th>

                        <th>
                            Insurance
                        </th>

                        <th>
                            Patient
                        </th>

                    </tr>

                </thead>


                <tbody>

                    ${procedureRows}

                </tbody>

            </table>


            <div class="totals">

                <div class="total-row">

                    <strong>
                        Total Procedure Cost
                    </strong>

                    <strong>
                        $${formatMoney(
                            verification.total_procedure_cost
                        )}
                    </strong>

                </div>


                <div class="total-row">

                    <strong>
                        Estimated Insurance Payment
                    </strong>

                    <strong>
                        $${formatMoney(
                            verification.total_estimated_insurance_payment
                        )}
                    </strong>

                </div>


                <div class="total-row">

                    <strong>
                        Estimated Patient Responsibility
                    </strong>

                    <strong>
                        $${formatMoney(
                            verification.total_estimated_patient_responsibility
                        )}
                    </strong>

                </div>

            </div>


            <h2>
                Policy Information
            </h2>


            <div class="info-grid">

                <div class="info-item">

                    <strong>
                        Annual Limit
                    </strong>

                    $${formatMoney(
                        policy.annual_limit
                    )}

                </div>


                <div class="info-item">

                    <strong>
                        Remaining Limit
                    </strong>

                    $${formatMoney(
                        policy.remaining_limit
                    )}

                </div>


                <div class="info-item">

                    <strong>
                        Deductible
                    </strong>

                    $${formatMoney(
                        policy.deductible
                    )}

                </div>


                <div class="info-item">

                    <strong>
                        Remaining Deductible
                    </strong>

                    $${formatMoney(
                        policy.deductible_remaining
                    )}

                </div>

            </div>


            <p style="margin-top: 40px; color: #64748b;">

                This report is generated by the
                DenSure hackathon prototype.
                Cost estimates are for demonstration
                purposes and do not represent actual
                insurance claim adjudication.

            </p>


            <script>

                window.onload = function () {
                    window.print();
                };

            <\/script>


        </body>

        </html>

    `);


    reportWindow.document.close();
}


// ==========================================
// SAVE VERIFICATION HISTORY
// ==========================================

function saveVerificationHistory(data) {

    const history =
        JSON.parse(
            localStorage.getItem(
                "dentalVerifyHistory"
            )
        ) || [];


    const verification =
        data.verification;


    const historyItem = {

        patientName:
            data.patient.name,

        memberId:
            data.patient.member_id,

        provider:
            data.patient.provider,

        procedureCount:
            verification.procedure_count,

        totalCost:
            verification.total_procedure_cost,

        insurancePayment:
            verification.total_estimated_insurance_payment,

        patientResponsibility:
            verification.total_estimated_patient_responsibility,

        status:
            verification.overall_status,

        time:
            new Date().toLocaleString()
    };


    history.unshift(
        historyItem
    );


    const limitedHistory =
        history.slice(0, 10);


    localStorage.setItem(
        "dentalVerifyHistory",
        JSON.stringify(
            limitedHistory
        )
    );
}


// ==========================================
// DISPLAY HISTORY
// ==========================================

function displayHistory() {

    const history =
        JSON.parse(
            localStorage.getItem(
                "dentalVerifyHistory"
            )
        ) || [];


    if (history.length === 0) {

        historyContainer.innerHTML = `

            <div class="empty-history">

                No verification history yet.

            </div>

        `;

        return;
    }


    historyContainer.innerHTML = "";


    history.forEach(function (item) {

        let statusClass =
            "history-not-eligible";


        if (item.status === "ELIGIBLE") {

            statusClass =
                "history-eligible";

        } else if (
            item.status === "NEEDS REVIEW"
        ) {

            statusClass =
                "history-review";
        }


        const historyItem =
            document.createElement(
                "div"
            );


        historyItem.className =
            "history-item";


        historyItem.innerHTML = `

            <div class="history-main">


                <div class="history-patient">

                    <strong>
                        ${escapeHtml(
                            item.patientName
                        )}
                    </strong>

                    <span>
                        ${escapeHtml(
                            item.memberId
                        )}
                    </span>

                </div>


                <div class="history-procedure">

                    <strong>
                        ${item.procedureCount}
                        Procedure(s)
                    </strong>

                    <span>
                        Total:
                        $${formatMoney(
                            item.totalCost
                        )}
                    </span>

                </div>


                <div>

                    <span class="history-status ${statusClass}">

                        ${escapeHtml(
                            item.status
                        )}

                    </span>

                </div>


                <div class="history-time">

                    ${escapeHtml(
                        item.time
                    )}

                </div>

            </div>

        `;


        historyContainer.appendChild(
            historyItem
        );
    });
}


// ==========================================
// CLEAR HISTORY
// ==========================================

clearHistoryButton.addEventListener(
    "click",
    function () {

        const confirmed =
            confirm(
                "Clear all verification history?"
            );


        if (!confirmed) {
            return;
        }


        localStorage.removeItem(
            "dentalVerifyHistory"
        );


        displayHistory();
    }
);


// ==========================================
// ERROR DISPLAY
// ==========================================

function showError(message) {

    result.innerHTML = `

        <div class="error-card">

            ${escapeHtml(message)}

        </div>

    `;


    reportActions.innerHTML = "";
}


// ==========================================
// MONEY FORMATTER
// ==========================================

function formatMoney(value) {

    const number =
        Number(value);


    if (Number.isNaN(number)) {
        return "0.00";
    }


    return number.toFixed(2);
}


// ==========================================
// REPORT STATUS CLASS
// ==========================================

function getReportStatusClass(status) {

    if (status === "ELIGIBLE") {
        return "eligible";
    }


    if (status === "NEEDS REVIEW") {
        return "review";
    }


    return "not-eligible";
}


// ==========================================
// HTML ESCAPE
// ==========================================

function escapeHtml(value) {

    if (
        value === null
        ||
        value === undefined
    ) {

        return "";
    }


    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}


// ==========================================
// LOAD HISTORY ON PAGE LOAD
// ==========================================

displayHistory();

"use strict";

// Class definition
var KTSigninGeneral = function () {
    // Elements
    var form;
    var submitButton;
    var validator;
    var loadingOverlay;

    // Handle form
    var handleValidation = function (e) {
        // Init form validation rules. For more info check the FormValidation plugin's official documentation:https://formvalidation.io/
        validator = FormValidation.formValidation(
            form,
            {
                fields: {
                    'usuario': {
                        validators: {
                            notEmpty: {
                                message: 'Campo Obligatorio'
                            }
                        }
                    },
                    'contraseña': {
                        validators: {
                            notEmpty: {
                                message: 'Campo Obligatorio'
                            }
                        }
                    }
                },
                plugins: {
                    trigger: new FormValidation.plugins.Trigger(),
                    bootstrap: new FormValidation.plugins.Bootstrap5({
                        rowSelector: '.fv-row',
                        eleInvalidClass: '',  // comment to enable invalid state icons
                        eleValidClass: '' // comment to enable valid state icons
                    })
                }
            }
        );
    }

    var handleSubmit = function (e) {
        // Handle form submit
        submitButton.addEventListener('click', function (e) {
            // Prevent button default action
            e.preventDefault();

            // Validate form
            validator.validate().then(function (status) {
                console.log(status)
                if (status == 'Valid') {
                    // Show loading indication
                    submitButton.setAttribute('data-kt-indicator', 'on');

                    // Disable button to avoid multiple click
                    submitButton.disabled = true;

                    // Create FormData object from form element
                    var formData = new FormData(form);

                    // Send data using fetch
                    fetch(form.action, {
                        method: 'POST',
                        body: formData,
                        headers: {
                            'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value
                        }
                    })
                    .then(response => {
                        console.log(response)
                        if (!response.ok) {
                            throw new Error('Network response was not ok');
                        }

                        return response.json();
                    })
                    .then(data => {
                        console.log(data)
                        // Hide loading indication
                        submitButton.removeAttribute('data-kt-indicator');

                        // Enable button
                        submitButton.disabled = false;
                        
                        if (data.success) {
                            // Show message popup with auto-close timer. For more info check the plugin's official documentation: https://sweetalert2.github.io/
                            Swal.fire({
                                text: "Datos Verificados Correctamente",
                                icon: "success",
                                buttonsStyling: false,
                                timer: 1000, // 3 seconds
                                showConfirmButton: false, // Hides the confirm button
                                customClass: {
                                    confirmButton: "btn btn-primary"
                                }
                            }).then(function () {
                                // Show page loading overlay after the modal closes
                                loadingOverlay.style.display = 'flex';
                                
                                // Redirect to the specified URL after the timer ends
                                var redirectUrl = form.getAttribute('data-kt-redirect-url');
                                if (redirectUrl) {
                                    location.href = redirectUrl;
                                } else {
                                    location.href = data.redirectUrl;
                                }
                            });
                        } else {
                            // Show error popup. For more info check the plugin's official documentation: https://sweetalert2.github.io/
                            Swal.fire({
                                text: data.message || "Sorry, the username or password is incorrect, please try again.",
                                icon: "error",
                                buttonsStyling: false,
                                confirmButtonText: "intentar de nuevo",
                                customClass: {
                                    confirmButton: "btn btn-primary"
                                }
                            });
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);

                        // Hide loading indication
                        submitButton.removeAttribute('data-kt-indicator');

                        // Enable button
                        submitButton.disabled = false;

                        // Show error popup. For more info check the plugin's official documentation: https://sweetalert2.github.io/
                        Swal.fire({
                            text: "Faltan campos obligatorios.",
                            icon: "error",
                            buttonsStyling: false,
                            confirmButtonText: "Intentar de nuevo",
                            customClass: {
                                confirmButton: "btn btn-primary"
                            }
                        });
                    });
                } else {
                    // Show error popup. For more info check the plugin's official documentation: https://sweetalert2.github.io/
                    Swal.fire({
                        text: "Faltan campos obligatorios.",
                        icon: "error",
                        buttonsStyling: false,
                        confirmButtonText: "Intentar de nuevo",
                        customClass: {
                            confirmButton: "btn btn-primary"
                        }
                    });
                }
            });
        });
    }

    // Public functions
    return {
        // Initialization
        init: function () {
            form = document.querySelector('#kt_sign_in_form');
            submitButton = document.querySelector('#kt_sign_in_submit');
            loadingOverlay = document.querySelector('#kt_page_loading_overlay');

            handleValidation();
            handleSubmit();
        }
    };
}();

// On document ready
KTUtil.onDOMContentLoaded(function () {
    KTSigninGeneral.init();
});

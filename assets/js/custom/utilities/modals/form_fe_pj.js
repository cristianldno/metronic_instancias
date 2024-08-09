document.addEventListener('DOMContentLoaded', function() {
    // Class definition
    var KTModalNewForm = function () {
        var submitButton;
        var cancelButton;
        var validator;
        var form;
        var modal;
        var modalEl;

        // Init form inputs
        var initForm = function() {
            // Due date. For more info, please visit the official plugin site: https://flatpickr.js.org/
            var dueDate = $(form.querySelector('[name="fecha-certificado"]'));
            dueDate.flatpickr({
                enableTime: true,
                dateFormat: "d, M Y, H:i",
            });

            // Department and Municipality select2. For more info, please visit the official plugin site: https://select2.org/
            $(form.querySelector('[name="departamento-persona"]')).on('change', function() {
                // Revalidate the field when an option is chosen
                validator.revalidateField('departamento-persona');
            });

            $(form.querySelector('[name="municipio-persona"]')).on('change', function() {
                // Revalidate the field when an option is chosen
                validator.revalidateField('municipio-persona');
            });

            $(form.querySelector('[name="departamento-empresa"]')).on('change', function() {
                // Revalidate the field when an option is chosen
                validator.revalidateField('departamento-empresa');
            });

            $(form.querySelector('[name="municipio-empresa"]')).on('change', function() {
                // Revalidate the field when an option is chosen
                validator.revalidateField('municipio-empresa');
            });
        }

        // Handle form validation and submission
        var handleForm = function() {
            // Init form validation rules. For more info check the FormValidation plugin's official documentation: https://formvalidation.io/
            validator = FormValidation.formValidation(
                form,
                {
                    fields: {
                        nombre: {
                            validators: {
                                notEmpty: {
                                    message: 'El nombre es obligatorio'
                                }
                            }
                        },
                        'numero-documento': {
                            validators: {
                                notEmpty: {
                                    message: 'El número de documento es obligatorio'
                                }
                            }
                        },
                        'correo': {
                            validators: {
                                notEmpty: {
                                    message: 'El correo es obligatorio'
                                },
                                emailAddress: {
                                    message: 'El valor no es una dirección de correo válida'
                                }
                            }
                        },
                        'direccion': {
                            validators: {
                                notEmpty: {
                                    message: 'La dirección es obligatoria'
                                }
                            }
                        }
                    },
                    plugins: {
                        trigger: new FormValidation.plugins.Trigger(),
                        bootstrap: new FormValidation.plugins.Bootstrap5({
                            rowSelector: '.fv-row',
                            eleInvalidClass: '',
                            eleValidClass: ''
                        })
                    }
                }
            );

            // Action buttons
            submitButton.addEventListener('click', function (e) {
                e.preventDefault();

                // Validate form before submit
                if (validator) {
                    validator.validate().then(function (status) {
                        console.log('validated!');

                        if (status == 'Valid') {
                            submitButton.setAttribute('data-kt-indicator', 'on');

                            // Disable button to avoid multiple clicks
                            submitButton.disabled = true;

                            setTimeout(function() {
                                submitButton.removeAttribute('data-kt-indicator');

                                // Enable button
                                submitButton.disabled = false;
                                
                                // Show success message. For more info check the plugin's official documentation: https://sweetalert2.github.io/
                                Swal.fire({
                                    text: "Datos enviados exitosamente!",
                                    icon: "success",
                                    buttonsStyling: false,
                                    confirmButtonText: "Finalizar",
                                    customClass: {
                                        confirmButton: "btn btn-primary"
                                    }
                                }).then(function (result) {
                                    if (result.isConfirmed) {
                                        modal.hide();
                                    }
                                });

                                // form.submit(); // Submit form
                            }, 2000);                         
                        } else {
                            // Show error message.
                            Swal.fire({
                                text: "Lo sentimos, parece que hay algunos errores detectados, por favor intente de nuevo.",
                                icon: "error",
                                buttonsStyling: false,
                                confirmButtonText: "Ok, entendido!",
                                customClass: {
                                    confirmButton: "btn btn-primary"
                                }
                            });
                        }
                    });
                }
            });

            cancelButton.addEventListener('click', function (e) {
                e.preventDefault();

                Swal.fire({
                    text: "¿Está seguro de que desea cancelar?",
                    icon: "warning",
                    showCancelButton: true,
                    buttonsStyling: false,
                    confirmButtonText: "Sí, cancelar!",
                    cancelButtonText: "No, volver",
                    customClass: {
                        confirmButton: "btn btn-primary",
                        cancelButton: "btn btn-active-light"
                    }
                }).then(function (result) {
                    if (result.value) {
                        form.reset(); // Reset form    
                        modal.hide(); // Hide modal                
                    } else if (result.dismiss === 'cancel') {
                        Swal.fire({
                            text: "Su formulario no ha sido cancelado!.",
                            icon: "error",
                            buttonsStyling: false,
                            confirmButtonText: "Ok, entendido!",
                            customClass: {
                                confirmButton: "btn btn-primary",
                            }
                        });
                    }
                });
            });
        }

        return {
            // Public functions
            init: function () {
                // Elements
                modalEl = document.getElementById('formulario_fe_pj');
                console.log('este es el modal:',modalEl)

                if (!modalEl) {
                    console.error('No se encontró el elemento modal #formulario_fe_pj');
                    return;
                }

                try {
                    modal = new bootstrap.Modal(modalEl);
                } catch (error) {
                    console.error('Error al inicializar el modal:', error);
                    return;
                }

                form = document.querySelector('#formulario_fe_pj_form');
                submitButton = document.getElementById('formulario_fe_pj_submit');
                cancelButton = document.getElementById('formulario_fe_pj_cancel');

                if (!form || !submitButton || !cancelButton) {
                    console.error('No se encontraron elementos form/submit/cancel correctamente');
                    return;
                }

                initForm();
                handleForm();
            }
        };
    }();

    // On document ready
    KTModalNewForm.init();
});
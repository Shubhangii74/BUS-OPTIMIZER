// Common JavaScript functions for Bus Seat Allocation Optimizer

// API Base URL
const API_BASE_URL = '';

// Utility Functions
const Utils = {
    // Show loading spinner
    showLoading: function(element) {
        if (element) {
            element.innerHTML = '<div class="spinner"></div>';
        }
    },

    // Hide loading spinner
    hideLoading: function(element, content) {
        if (element) {
            element.innerHTML = content || '';
        }
    },

    // Show alert message
    showAlert: function(message, type = 'info', container = null) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type}`;
        alertDiv.innerHTML = message;
        
        if (container) {
            container.insertBefore(alertDiv, container.firstChild);
        } else {
            document.body.insertBefore(alertDiv, document.body.firstChild);
        }

        // Auto remove after 5 seconds
        setTimeout(() => {
            alertDiv.remove();
        }, 5000);
    },

    // Format date
    formatDate: function(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
    },

    // Validate email
    validateEmail: function(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    },

    // Debounce function
    debounce: function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
};

// API Functions
const API = {
    // Generic fetch function
    fetch: async function(url, options = {}) {
        try {
            const response = await fetch(API_BASE_URL + url, {
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                },
                ...options
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    },

    // Get routes
    getRoutes: async function() {
        return await this.fetch('/api/routes');
    },

    // Get bookings
    getBookings: async function() {
        return await this.fetch('/api/bookings');
    },

    // Get buses
    getBuses: async function() {
        return await this.fetch('/api/buses');
    },

    // Book seat
    bookSeat: async function(bookingData) {
        return await this.fetch('/api/book', {
            method: 'POST',
            body: JSON.stringify(bookingData)
        });
    }
};

// Modal Functions
const Modal = {
    // Show modal
    show: function(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.style.display = 'block';
            document.body.style.overflow = 'hidden';
        }
    },

    // Hide modal
    hide: function(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.style.display = 'none';
            document.body.style.overflow = 'auto';
        }
    },

    // Initialize modal close events
    init: function() {
        // Close on X click
        document.querySelectorAll('.close').forEach(closeBtn => {
            closeBtn.addEventListener('click', function() {
                const modal = this.closest('.modal');
                if (modal) {
                    Modal.hide(modal.id);
                }
            });
        });

        // Close on outside click
        window.addEventListener('click', function(event) {
            if (event.target.classList.contains('modal')) {
                Modal.hide(event.target.id);
            }
        });

        // Close on Escape key
        document.addEventListener('keydown', function(event) {
            if (event.key === 'Escape') {
                const visibleModal = document.querySelector('.modal[style*="display: block"]');
                if (visibleModal) {
                    Modal.hide(visibleModal.id);
                }
            }
        });
    }
};

// Form Validation
const FormValidator = {
    // Validate required fields
    validateRequired: function(fields) {
        const errors = [];
        fields.forEach(field => {
            const element = document.getElementById(field.id);
            if (!element || !element.value.trim()) {
                errors.push(field.message || `${field.id} is required`);
            }
        });
        return errors;
    },

    // Validate email
    validateEmailField: function(emailFieldId) {
        const emailField = document.getElementById(emailFieldId);
        if (emailField && !Utils.validateEmail(emailField.value)) {
            return 'Please enter a valid email address';
        }
        return null;
    },

    // Clear form
    clearForm: function(formId) {
        const form = document.getElementById(formId);
        if (form) {
            form.reset();
        }
    }
};

// Animation Functions
const Animations = {
    // Initialize AOS
    initAOS: function() {
        if (typeof AOS !== 'undefined') {
            AOS.init({
                duration: 1000,
                once: true,
                offset: 100
            });
        }
    },

    // Fade in elements on scroll
    initScrollAnimations: function() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                }
            });
        }, observerOptions);

        // Observe elements with animation classes
        document.querySelectorAll('.fade-in, .slide-in-left, .slide-in-right').forEach(el => {
            observer.observe(el);
        });
    },

    // Add loading animation to button
    addButtonLoading: function(button, text = 'Loading...') {
        const originalText = button.innerHTML;
        button.disabled = true;
        button.innerHTML = `<i class="fas fa-spinner fa-spin"></i> ${text}`;
        return () => {
            button.disabled = false;
            button.innerHTML = originalText;
        };
    }
};

// Bus Layout Functions
const BusLayout = {
    // Generate seat layout HTML
    generateSeatLayout: function(busNumber, bookedSeats = []) {
        const seatRows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'];
        const seatCols = [1, 2, 3, 4];
        let layout = '';

        seatRows.forEach(row => {
            seatCols.forEach(col => {
                const seatNumber = `${row}${col}`;
                const isBooked = bookedSeats.includes(seatNumber);
                const seatClass = isBooked ? 'seat booked' : 'seat available';
                layout += `<div class="seat ${seatClass}" data-seat="${seatNumber}" data-bus="${busNumber}">${seatNumber}</div>`;
            });
        });

        return layout;
    },

    // Update seat status
    updateSeatStatus: function(busNumber, bookedSeats) {
        const seatElements = document.querySelectorAll(`[data-bus="${busNumber}"]`);
        seatElements.forEach(seat => {
            const seatNumber = seat.dataset.seat;
            const isBooked = bookedSeats.includes(seatNumber);
            seat.className = isBooked ? 'seat booked' : 'seat available';
        });
    },

    // Get booked seats for a bus
    getBookedSeatsForBus: function(bookings, busNumber) {
        return bookings
            .filter(booking => booking.BusNumber === busNumber && booking.Status === 'Confirmed')
            .map(booking => booking.SeatNumber);
    }
};

// Statistics Functions
const Statistics = {
    // Calculate booking statistics
    calculateStats: function(bookings, buses) {
        const totalBookings = bookings.length;
        const totalSeats = buses.reduce((sum, bus) => sum + parseInt(bus.TotalSeats), 0);
        const bookedSeats = buses.reduce((sum, bus) => sum + parseInt(bus.BookedSeats), 0);
        const availableSeats = totalSeats - bookedSeats;

        return {
            totalBookings,
            totalBuses: buses.length,
            totalSeats,
            bookedSeats,
            availableSeats,
            occupancyRate: totalSeats > 0 ? (bookedSeats / totalSeats * 100).toFixed(1) : 0
        };
    },

    // Update statistics display
    updateStatsDisplay: function(stats) {
        const elements = {
            totalBookings: document.getElementById('totalBookings'),
            totalBuses: document.getElementById('totalBuses'),
            totalSeats: document.getElementById('totalSeats'),
            availableSeats: document.getElementById('availableSeats')
        };

        if (elements.totalBookings) elements.totalBookings.textContent = stats.totalBookings;
        if (elements.totalBuses) elements.totalBuses.textContent = stats.totalBuses;
        if (elements.totalSeats) elements.totalSeats.textContent = stats.totalSeats;
        if (elements.availableSeats) elements.availableSeats.textContent = stats.availableSeats;
    }
};

// Initialize common functionality
document.addEventListener('DOMContentLoaded', function() {
    // Initialize modals
    Modal.init();

    // Initialize animations
    Animations.initAOS();
    Animations.initScrollAnimations();

    // Add smooth scrolling to anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        Utils,
        API,
        Modal,
        FormValidator,
        Animations,
        BusLayout,
        Statistics
    };
} 
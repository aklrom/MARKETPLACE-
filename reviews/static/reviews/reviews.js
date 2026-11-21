// static/reviews/reviews.js
document.addEventListener('DOMContentLoaded', function() {
    const textarea = document.querySelector('textarea[name="text"]');

    if (textarea) {
        const autoResize = () => {
            textarea.style.height = 'auto';
            textarea.style.height = `${textarea.scrollHeight}px`;
        };

        textarea.addEventListener('input', autoResize);
        autoResize();
    }

    const ratingGroup = document.querySelector('.rating-control__stars');
    if (!ratingGroup) {
        return;
    }

    const feedback = document.querySelector('[data-rating-feedback]');
    const inputs = ratingGroup.querySelectorAll('input[type="radio"]');
    const updateFeedback = (value) => {
        feedback.textContent = value
            ? `${value} étoile${value === '1' ? '' : 's'}`
            : 'Choisir une note';
    };

    inputs.forEach((input) => {
        input.addEventListener('change', () => updateFeedback(input.value));
        input.addEventListener('focus', () => updateFeedback(input.value));
    });

    ratingGroup.querySelectorAll('.rating-control__star').forEach((star) => {
        star.addEventListener('mouseenter', () => {
            updateFeedback(star.dataset.rating);
        });
    });

    ratingGroup.addEventListener('mouseleave', () => {
        const selected = ratingGroup.querySelector('input:checked');
        updateFeedback(selected ? selected.value : '');
    });
});
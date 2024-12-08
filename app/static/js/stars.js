document.addEventListener('DOMContentLoaded', function() {
    const ratingStars = document.querySelectorAll('.rating-stars');
    
    ratingStars.forEach(container => {
        let rating = parseFloat(container.dataset.rating);
        
        // Validate and clamp the rating between 0 and 5
        if (isNaN(rating)) rating = 0;
        rating = Math.max(0, Math.min(5, rating));
        
        const stars = container.querySelectorAll('.star');
        
        stars.forEach((star, index) => {
            const position = index + 1;
            let fillPercentage = 0;
            
            if (position <= Math.floor(rating)) {
                // Full star
                fillPercentage = 100;
            } else if (position === Math.ceil(rating)) {
                // Partial star - use toFixed(4) for precise decimal handling
                fillPercentage = ((rating % 1) * 100).toFixed(4);
            }
            
            // Set the width of the filled star with a smooth transition
            requestAnimationFrame(() => {
                star.style.setProperty('--fill-percentage', `${fillPercentage}%`);
            });
        });
    });
});

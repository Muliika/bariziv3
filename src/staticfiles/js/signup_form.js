document.addEventListener('DOMContentLoaded', function() {
    // Get the user type radio buttons and business category field
    const userTypeInputs = document.querySelectorAll('input[name="user_type"]');
    const businessCategoryGroup = document.getElementById('business_category_group');
    
    // Function to update visibility of business category field
    function updateCategoryVisibility() {
        const selectedUserType = document.querySelector('input[name="user_type"]:checked');
        
        if (selectedUserType && selectedUserType.value === 'business') {
            businessCategoryGroup.style.display = 'block';
        } else {
            businessCategoryGroup.style.display = 'none';
        }
    }
    
    // Set initial state
    updateCategoryVisibility();
    
    // Add event listeners to user type radio buttons
    userTypeInputs.forEach(input => {
        input.addEventListener('change', updateCategoryVisibility);
    });
});
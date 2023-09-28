document.addEventListener("DOMContentLoaded", function() {
    const hashtagCheckboxes = document.querySelectorAll(".related-widget-wrapper select[multiple] option");
    
    function updateHashtagList() {
        let tagContainer = document.querySelector(".hashtag-tags");
        if (!tagContainer) {
            tagContainer = document.createElement("div");
            tagContainer.className = "hashtag-tags";
            document.querySelector(".related-widget-wrapper").appendChild(tagContainer);
        }
        tagContainer.innerHTML = "";
        hashtagCheckboxes.forEach(checkbox => {
            if (checkbox.selected) {
                const tagLabel = document.createElement("span");
                tagLabel.className = "hashtag-tag";
                tagLabel.innerText = checkbox.innerText;
                tagContainer.appendChild(tagLabel);
            }
        });
    }

    hashtagCheckboxes.forEach(checkbox => {
        checkbox.addEventListener("click", updateHashtagList);
    });

    updateHashtagList();
});

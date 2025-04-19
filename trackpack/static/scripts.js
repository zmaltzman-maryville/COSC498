// Dynamically filter packages on page
function filterPackages() {
    // Get values from all filter inputs
    var all_filters = document.querySelector("#filter_container").querySelectorAll('.package_value');
    var filters = {};

    // Add inputs that aren't empty to object of filters
    for (var i = 0; i < all_filters.length; i++) {
        var input = all_filters[i];
        if (input.value != "") {
            filters[input.classList[1]] = input.value.toUpperCase();
        }
    }

    // Find all packages
    var packages = document.querySelectorAll(".package_container");
    // Iterate over each package
    for (var i = 0; i < packages.length; i++) {
        var mismatch = false;
        // Iterate over each non-empty filter
        for (var filter in filters) {
            try {
                var target = filters[filter];
                var property = packages[i].querySelector("." + filter).innerHTML.toUpperCase();
                if (!property.match(`${target}`)) {
                    mismatch = true;
                }
            } catch {
                mismatch = true;
            }
        }

        // If string didn't have a match in the same property field, hide package
        if (mismatch) {
            packages[i].style.display = "none";
        } else {
            packages[i].style.display = "";
        }
    }
}

// Clear filters and show all packages again
function clearFilters() {
    // Empty out filter inputs
    var all_filters = document.querySelector("#filter_container").querySelectorAll('.package_value');
    for (var filter in all_filters) {
        all_filters[filter].value = "";
    }

    // Show all packages
    var packages = document.querySelectorAll(".package_container");
    for (var i = 0; i < packages.length; i++) {
        packages[i].style.display = "";
    }
}

// Toggle visibility of filter container
function toggleFilters() {
    // Fetch the containers
    var filters = document.querySelector("#filter_container");
    var showing = window.getComputedStyle(filters).getPropertyValue('display');
    var collapsed = document.querySelector("#filter_collapsed");
    
    // Invert visibility
    if (showing == 'none') {
        collapsed.style.display = "none";
        filters.style.display = "block";
    } else {
        collapsed.style.display = "block";
        filters.style.display = "none";
    }
}

// Elements from the flash method have no native removal method
function dismissFlash() {
    var flash = document.querySelector("#flash_container");
    flash.remove();
}
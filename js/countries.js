

    function getCities(){
        var inputCity = document.getElementById('cities').value;
        const city = changeCase(inputCity);

        if(city.length <= 2){
            return false;
        }

        // Create request to get cities locations
        var request = new XMLHttpRequest();
        request.addEventListener("load", transferComplete);
        request.open("GET", "/cities/?cityname=" + city);
        request.send();

        // Called when transfer is complete
        function transferComplete(event){
            locations = JSON.parse(event.srcElement.response);
            // Return false if no matching city was found
            if(locations.length == 0){
                return false;
            }

            // Append choices 
            dropContent = document.getElementById('cities-dropdown-content');
            
            dropContent.innerHTML = "";
            for (var i = 0; i < locations.length; i++) {
                var link = document.createElement("a");
                link.setAttribute("onclick", "setCity(" + JSON.stringify(locations[i].name) + "," + JSON.stringify(locations[i].state) + "," + JSON.stringify(locations[i].country) + ")");
                link.setAttribute("class", "dropdown-item");
                //link.setAttribute("tabindex", i);
                link.innerHTML = locations[i].name + ", " + locations[i].state.name + ", " + locations[i].country.name
                dropContent.append(link);
            }
            // dropContent.setFocus;
            // document.getElementsByClassName('dropdown-item')[1].setFocus;
            document.getElementById("cities-dropdown").classList.add("is-active");
        }
    }

    function setCity(city, state, country){
        document.getElementById('cities').value = city+', '+state.name+', '+country.name;
        document.getElementById('city').value = city;
        document.getElementById('state').value = state.name;
        document.getElementById('country').value = country.name;
        document.getElementById('cities-dropdown-content').innerHTML = "";
        document.getElementById("cities-dropdown").classList.remove("is-active");
    }

    function clearCities(){
        document.getElementById('cities-dropdown-content').innerHTML = "";
        document.getElementById("cities-dropdown").classList.remove("is-active");
    }

    function deleteEntry(e){
        e.preventDefault();
        document.getElementById('cities').value = '';
    }

    function changeCase(inputCity){
        return inputCity
               .replace(/([a-z])([A-Z])/g, function (allMatches, firstMatch, secondMatch) {
                     return firstMatch + " " + secondMatch;
               })
               .toLowerCase()
               .replace(/([ -_]|^)(.)/g, function (allMatches, firstMatch, secondMatch) {
                     return (firstMatch ? " " : "") + secondMatch.toUpperCase();
               }
        );
    }
    var eraser = document.getElementById("clear");
    eraser.addEventListener('click', deleteEntry);
    
    /*var citiesWidget = document.getElementById("cities");
    citiesDropDown = document.getElementById("cities-dropdown-content");
    
    citiesWidget.addEventListener('keypress', function(e) {
        var code = e.which || e.keyCode;
        if (code == '38') {
            // Up
            citiesDropDown.setFocus();
        }
        else if (code == '40') {
            // Down
            document.getElementsByClassName('dropdown-item')[1].setFocus();
        }
    })*/


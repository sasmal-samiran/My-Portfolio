/***DOM ELEMENTS***/
// Backend API
BACKEND_API = 'https://codecraftedbysam.onrender.com/travelplanner/weather';

const inputCity = document.querySelector('#input-city');
const searchButton = document.querySelector('#search-button');
const cityName = document.querySelector('#city-name');
const weatherDetails = document.querySelector('.weather-details');
const temperature = document.querySelector('#temperature');
const apparentTemperature = document.querySelector('#apparent-temperature');
const weathercode = document.querySelector('#weathercode');
const weatherIcons = document.querySelectorAll('#weather-icon');
const currentTime = document.querySelector('#current-time');
const isDay = document.querySelector('#is-day');
const paraTemperature = document.querySelector('.parameters.temperature');
const paraPrecipitation = document.querySelector('.parameters.precipitation');
const paraRain = document.querySelector('.parameters.rain');
const paraDew = document.querySelector('.parameters.dew');
const paraHumidity = document.querySelector('.parameters.humidity');
const paraSnow = document.querySelector('.parameters.snow');
const paraVisibility = document.querySelector('.parameters.visibility');
const dataDiv = document.querySelectorAll('.data-div');
const hiddenDiv = document.querySelectorAll('.hidden-div');

const inputRange = document.querySelector('.user-input #range-input');
const inputRangeValue = document.querySelector('.user-input #range-value');
inputRange.addEventListener("input", (event) => {
    inputRangeValue.textContent = event.target.value;
});

const historical_places = document.querySelector('.historical_places');
const natural_places = document.querySelector('.natural_places');
const religious_places = document.querySelector('.religious_places');
const entertainment_places = document.querySelector('.entertainment_places');
const food_places = document.querySelector('.food_places');
const shopping_places = document.querySelector('.shopping_places');

let city = inputCity.value.trim().toUpperCase();
/***FUNCTIONS ***/
async function getLocation() {
    return new Promise((resolve, reject) => {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                resolve({
                    currentLat: position.coords.latitude,
                    currentLon: position.coords.longitude
                });
            },
            (error) => {
                resolve({
                    currentLat: 28.6139,
                    currentLon: 77.2090
                });
            }
        );
    });
}

function createAttractionCard(data) {
    const card = document.createElement('div');
    card.className = 'attractions-cards';
    card.innerHTML = `
        <div class="attractions-image">
            <div id="image"></div>
        </div>
        <div class="card-details">
            <h3 id="name">${data.name || 'Unknown'}</h3>
            <div class="heading">
                <h4>Category</h4>
                <p id="category">${data.category || 'N/A'}</p>
            </div>
            <div class="heading">
                <h4>Distance</h4>
                <p><span id="distance">${data.distance || '0'}</span> km</p>
            </div>
            <div class="heading">
                <h4>Location</h4>
                <p id="location">${data.location || 'Not available'}</p>
            </div>
        </div>
        <div class="attractions-wikipedia">
            <a href="${data.wikipedia || '#'}" id="wikipedia-link" target="_blank">View Details</a>
        </div>
    `;

    return card;
}

async function weatherReport(city) {
    const { currentLat, currentLon } = await getLocation();
    radius = inputRange.value * 1000;
    try {
        let params = {
            'city': city,
            'currentLat': currentLat,
            'currentLon': currentLon,
            'radius': radius
        }
        const response = await fetch(BACKEND_API, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(params)
        });
        if (!response.ok) {
            throw new Error(`HTTP Error: ${response.status}`);
        }
        const data = await response.json();

        cityName.innerText = data.name.toUpperCase();
        currentTime.innerText = `As of ${data.current_time} IST`;
        weatherIcons.forEach(icon => {
            icon.style.display = 'none';
        });
        if (data.is_day) {
            isDay.innerText = 'Day';
            weatherIcons[data.weathercode[1] - 1].style.display = 'block';
        } else {
            isDay.innerText = 'Night';
            weatherIcons[data.weathercode[1] - 1 + 8].style.display = 'block';
        }

        temperature.innerText = data.temperature + 'ºC';
        apparentTemperature.innerText = `Feels like ${data.apparent_temperature} ºC`;
        weathercode.innerText = data.weathercode[0];
        weatherDetails.innerText = `Wind: ${data.wind} Km/h\nLatitude: ${data.lat} ºN\nLongitude: ${data.lon} ºE`;

        paraTemperature.innerText = `${data.temp_max}º / ${data.temp_min}º`;
        paraPrecipitation.innerText = `${data.precipitation} %`;
        paraRain.innerText = `${data.rain} mm`;
        paraDew.innerText = `${data.dew} ºC`;
        paraHumidity.innerText = `${data.humidity} %`;
        paraSnow.innerText = `${data.snow} cm`;
        paraVisibility.innerText = `${data.visibility} km`;

        const historicalPlaces = data.historical_places;
        historical_places.innerHTML = '';
        historicalPlaces.forEach(place => {
            const card = createAttractionCard(place);
            historical_places.appendChild(card);
        });
        const naturalPlaces = data.natural_places;
        natural_places.innerHTML = '';
        naturalPlaces.forEach(place => {
            const card = createAttractionCard(place);
            natural_places.appendChild(card);
        });
        const religiousPlaces = data.religious_places;
        religious_places.innerHTML = '';
        religiousPlaces.forEach(place => {
            const card = createAttractionCard(place);
            religious_places.appendChild(card);
        });
        const entertainmentPlaces = data.entertainment_places;
        entertainment_places.innerHTML = '';
        entertainmentPlaces.forEach(place => {
            const card = createAttractionCard(place);
            entertainment_places.appendChild(card);
        });
        const foodPlaces = data.food_places;
        food_places.innerHTML = '';
        foodPlaces.forEach(place => {
            const card = createAttractionCard(place);
            food_places.appendChild(card);
        });
        const shoppingPlaces = data.shopping_places;
        shopping_places.innerHTML = '';
        shoppingPlaces.forEach(place => {
            const card = createAttractionCard(place);
            shopping_places.appendChild(card);
        });
    } catch (error) {
        console.error("Error fetching weather:", error);
        weatherDetails.innerText = "Failed to fetch data. Please try again.";
    }
}

/*** EVENT LISTENERS ***/
weatherReport(city);
searchButton.addEventListener('click', async () => {
    city = inputCity.value.trim().toUpperCase();
    dataDiv.forEach(div => {
        div.style.display = 'none';
    })
    hiddenDiv.forEach(div => {
        div.style.display = 'block';
        div.innerText = `Searching for ${city}...`;
    })
    await weatherReport(city);
    dataDiv.forEach(div => {
        div.style.display = 'flex';
    })
    hiddenDiv.forEach(div => {
        div.style.display = 'none';
        div.innerText = ``;
    })
});
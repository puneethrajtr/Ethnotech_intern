async function getWeather() {
  let city = document.getElementById("city").value.trim();
  if (city === "") {
    document.getElementById("result").innerHTML = "⚠ Please enter a city name.";
    return;
  }

  let apiKey = "123f8d3104642907a26229e9ccedbdff"; // replace with your real key
  let url = `https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${apiKey}&units=metric`;

  try {
    let response = await fetch(url);
    let data = await response.json();
    console.log(data); // 👈 debug: see full response in browser console

    if (data.cod === 200) {
      document.getElementById("result").innerHTML = `
        <h3>${data.name}, ${data.sys.country}</h3>
        🌡 Temp: ${data.main.temp} °C <br>
        💧 Humidity: ${data.main.humidity}% <br>
        🌍 Condition: ${data.weather[0].description}
      `;
    } else {
      document.getElementById("result").innerHTML = `❌ ${data.message}`;
    }
  } catch (error) {
    console.error("Error fetching weather:", error);
    document.getElementById("result").innerHTML = "⚠ Something went wrong!";
  }
}

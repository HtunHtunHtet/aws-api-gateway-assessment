const fetch = require('node-fetch');

exports.handler = async (event) => {
    const city = event.queryStringParameters?.city || 'London';
    const apiKey = process.env.OPENWEATHER_API_KEY;

    try {
        const response = await fetch(`https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${apiKey}`);
        const data = await response.json();

        return {
            statusCode: 200,
            body: JSON.stringify({
                temperature: data.main.temp,
                weather: data.weather[0].description
            }),
        };
    } catch (err) {
        return {
            statusCode: 500,
            body: JSON.stringify({ error: err.message }),
        };
    }
};

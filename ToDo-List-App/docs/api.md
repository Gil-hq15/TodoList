## 🚀 API Integration: NASA APOD

Upon successful login, the app fetches the Astronomy Picture of the Day (APOD) using the NASA APOD API. This feature demonstrates how external APIs can enrich user experiences.

## Endpoint

- **URL**: `https://api.nasa.gov/planetary/apod`
- **API Key**: You must sign up at NASA's API portal to get an API key.

Example API response:

```json
{
  "date": "2024-12-10",
  "explanation": "This is an image of the day...",
  "url": "https://example.com/space-image.jpg"
}
```
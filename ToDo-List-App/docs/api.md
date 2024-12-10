# API Integration

The To-Do List App integrates with the NASA Astronomy Picture of the Day API to provide space images.

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
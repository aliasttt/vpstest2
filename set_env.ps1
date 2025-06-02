# Set environment variables for the project
$env:DJANGO_SECRET_KEY = "your-secret-key-here"
$env:DJANGO_DEBUG = "True"
$env:DJANGO_ALLOWED_HOSTS = "127.0.0.1,localhost"

# Payment Gateway Settings
$env:IYZICO_API_KEY = "your-api-key-here"
$env:IYZICO_SECRET_KEY = "your-secret-key-here"

# Email Settings
$env:EMAIL_HOST_USER = "your-email@gmail.com"
$env:EMAIL_HOST_PASSWORD = "your-app-password"

Write-Host "Environment variables have been set successfully!"
Write-Host "Please replace the placeholder values with your actual credentials." 
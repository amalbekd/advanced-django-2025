from django.db import models

class Resume(models.Model):
    user_email = models.EmailField(default="default@example.com")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='resumes/')
    analyzed = models.BooleanField(default=False)

    def __str__(self):
        return f"Resume from {self.user_email}"

class AnalysisResult(models.Model):
    resume = models.OneToOneField(Resume, on_delete=models.CASCADE)
    skills = models.TextField()
    summary = models.TextField()
    recommendations = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Analysis for {self.resume.user_email}"

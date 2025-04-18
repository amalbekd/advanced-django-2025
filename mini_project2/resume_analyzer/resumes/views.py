from rest_framework import viewsets
from .models import Resume, AnalysisResult
from .serializers import ResumeSerializer, AnalysisResultSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from .parser import extract_text_from_pdf, extract_text_from_docx
from .nlp_utils import analyze_resume_text
import os
from .ai.feedback import analyze_resume_feedback
from rest_framework.exceptions import ValidationError

class ResumeViewSet(viewsets.ModelViewSet):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer

class AnalysisResultViewSet(viewsets.ModelViewSet):
    queryset = AnalysisResult.objects.all()
    serializer_class = AnalysisResultSerializer


class ResumeAnalyzeView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, format=None):
        try:
            # Проверяем наличие файла в запросе
            file_obj = request.FILES.get('resume')
            if not file_obj:
                raise ValidationError("No resume file provided.")

            ext = os.path.splitext(file_obj.name)[1].lower()

            # Сохраняем файл во временную папку
            tmp_file_path = f"/tmp/{file_obj.name}"
            with open(tmp_file_path, "wb+") as f:
                for chunk in file_obj.chunks():
                    f.write(chunk)

            # Обработка в зависимости от типа файла
            if ext == '.pdf':
                raw_text = extract_text_from_pdf(tmp_file_path)
            elif ext in ['.docx', '.doc']:
                raw_text = extract_text_from_docx(tmp_file_path)
            else:
                return Response({"error": "Unsupported file format"}, status=400)

            # Обработка текста резюме
            parsed_data = analyze_resume_text(raw_text)

            # Получаем описание вакансии и даем обратную связь
            job_description = request.data.get("job_description", "")
            feedback = analyze_resume_feedback(parsed_data, job_description)

            return Response({
                "parsed_data": parsed_data,
                "feedback": feedback
            })

        except Exception as e:
            # Обработка непредвиденных ошибок
            return Response({"error": str(e)}, status=500)
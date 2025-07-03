from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import CatalogRAGQuery
from .serializers import CatalogRAGQuerySerializer
from .query_rag import ask_ai

class CatalogRAGQueryViewSet(viewsets.ModelViewSet):
    queryset = CatalogRAGQuery.objects.all().order_by('-created_at')
    serializer_class = CatalogRAGQuerySerializer

    def create(self, request, *args, **kwargs):
        question = request.data.get('question')
        if not question:
            return Response({'error': 'Missing question field.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            answer = ask_ai(question)
            rag_query = CatalogRAGQuery.objects.create(question=question, answer=answer)
            serializer = self.get_serializer(rag_query)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from rest_framework import serializers
from .models import Module, Section, Concept, UserProgress, QuizQuestion, QuizAttempt


class ConceptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Concept
        fields = ['id', 'name']


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ['id', 'order', 'title', 'content_md', 'has_visualizer',
                  'visualizer_type', 'key_insight']


class ModuleListSerializer(serializers.ModelSerializer):
    concepts = ConceptSerializer(many=True, read_only=True)
    section_count = serializers.SerializerMethodField()

    class Meta:
        model = Module
        fields = ['id', 'order', 'title', 'subtitle', 'description', 'difficulty',
                  'tag', 'icon', 'color', 'slug', 'estimated_time',
                  'section_count', 'concepts']

    def get_section_count(self, obj):
        return obj.sections.count()


class ModuleDetailSerializer(serializers.ModelSerializer):
    sections = SectionSerializer(many=True, read_only=True)
    concepts = ConceptSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = '__all__'


class UserProgressSerializer(serializers.ModelSerializer):
    module_title = serializers.CharField(source='module.title', read_only=True)
    module_slug = serializers.CharField(source='module.slug', read_only=True)

    class Meta:
        model = UserProgress
        fields = ['id', 'module', 'module_title', 'module_slug', 'section',
                  'completed', 'score', 'time_spent', 'last_accessed', 'started_at']


class QuizQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizQuestion
        fields = ['id', 'question_type', 'question', 'option_a', 'option_b',
                  'option_c', 'option_d', 'difficulty', 'order']
        # Note: correct_answer excluded for security, returned only after submission


class QuizSubmitSerializer(serializers.Serializer):
    answers = serializers.DictField(child=serializers.CharField(), help_text='{"question_id": "answer_choice"}')
    time_taken = serializers.IntegerField(min_value=0)


class QuizAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizAttempt
        fields = '__all__'

from django.shortcuts import render, redirect
from .forms import SchoolInquiryForm
from .models import SchoolInquiry
from modules.models import Module

FAQ_ITEMS = [
    (
        "Is there a free trial for schools?",
        "Yes. We offer a 14-day full-access trial for up to 10 students — no credit card required. Book a demo and we'll set it up within 24 hours."
    ),
    (
        "How do students join a classroom?",
        "Teachers share an 8-character join code (e.g. AILAB8C3) via WhatsApp or on the board. Students visit the join URL on any browser — no app download needed."
    ),
    (
        "Which boards / curricula does AI Lab follow?",
        "Content is aligned with CBSE and ICSE frameworks and maps to the emerging AI curriculum guidelines from NEP 2020. State board schools also find the content directly applicable."
    ),
    (
        "Do students need any prior coding knowledge?",
        "No. Class 8–10 tracks start from absolute basics (logic gates, patterns, sorting). Coding concepts are introduced gradually. Class 11–12 tracks go into practical AI implementation."
    ),
    (
        "How is progress tracked?",
        "Teachers get a real-time dashboard showing XP earned, modules completed, streaks, and assignment completion per student. Reports can be exported to CSV in one click."
    ),
    (
        "What is the Claude AI integration?",
        "Students can chat live with Anthropic's Claude AI model — the same technology powering enterprise AI tools. This is not a chatbot; it's the real thing, contextualised for learning."
    ),
    (
        "Can we customize the content for our school?",
        "Enterprise plans include custom module content and the ability to add school-specific case studies. School-plan customers can request content additions via WhatsApp support."
    ),
    (
        "What payment methods are accepted?",
        "We accept bank transfer (NEFT/RTGS), UPI, and Razorpay payment links. Schools can request a GST invoice. No international card required."
    ),
]


def landing_page(request):
    if request.method == 'POST':
        form = SchoolInquiryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/welcome/thank-you/')
    else:
        form = SchoolInquiryForm()

    modules = Module.objects.filter(is_published=True).order_by('order')[:7]
    inquiry_count = SchoolInquiry.objects.count()

    return render(request, 'landing/index.html', {
        'form': form,
        'modules': modules,
        'inquiry_count': inquiry_count,
        'faq_items': FAQ_ITEMS,
    })


def thank_you(request):
    return render(request, 'landing/thank_you.html')

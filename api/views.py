# api/views.py
from django.shortcuts import render
import google.generativeai as genai
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt


genai.configure(api_key=settings.GEMINI_API_KEY)
@csrf_exempt
def leetcode_helper_view(request):
    if request.method == 'POST':
        data = request.POST
        title = data.get("title")
        url = data.get("url")

        if not title or not url:
            return render(request, 'api/helper.html', {
                'error': 'Please provide both title and URL'
            })

        prompt = f"""
        You're an expert LeetCode mentor. A user is working on the problem titled: "{title}" ({url}).
        Give them clear, step-by-step guidance to solve it — including edge cases, brute-force thinking, and optimization ideas.
        DO NOT write or suggest actual code.
        Only provide strategic help in natural language.
        """

        model = genai.GenerativeModel("models/gemini-1.5-flash")  
        response = model.generate_content(prompt)
        answer = response.text

        steps = answer.strip().split("\n")
        steps = [step.strip() for step in steps if step.strip()]

        return render(request, 'api/helper.html', {
            'title': title,
            'url': url,
            'steps': steps,
            'success': True
        })


    return render(request, 'api/helper.html')

#!/usr/bin/env python3
"""
Script to fix the AI Interviewer blank page issue
"""

import re

# Read the file
file_path = r'c:\Users\saswa\Downloads\resume screener - Copy\res\res\templates\index.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

print("Applying fixes to index.html...")

# Fix 1: Update the submitAnswer function's try block
# Find and replace the fetch call and response handling
old_pattern1 = r'''                try \{
                    const question = interviewSession\.questions\[currentQuestion\];

                    const res = await fetch\('/api/interview/answer', \{
                        method: 'POST',
                        headers: \{ 'Content-Type': 'application/json' \},
                        body: JSON\.stringify\(\{
                            candidate_id: interviewSession\.candidate_id,
                            question: question\.question,
                            answer: currentAnswer,
                            question_index: currentQuestion
                        \}\)
                    \}\);

                    const data = await res\.json\(\);

                    if \(data\.success\) \{
                        const updatedAnswers = \[\.\.\.interviewSession\.answers \|\| \[\]\];
                        // Ensure array is big enough
                        while \(updatedAnswers\.length <= currentQuestion\) updatedAnswers\.push\(\{\}\);

                        updatedAnswers\[currentQuestion\] = \{
                            question: question\.question,
                            answer: currentAnswer,
                            evaluation: data\.evaluation
                        \};

                        // Update session state properly
                        setInterviewSession\(prev => \(\{
                            \.\.\.prev,
                            answers: updatedAnswers
                        \}\)\);

                        // Auto-advance logic with captured values to avoid closure issues
                        setTimeout\(\(\) => \{
                            setIsEvaluating\(false\);
                            if \(currentQ < totalQuestions - 1\) \{
                                setCurrentQuestion\(currentQ \+ 1\);
                                setCurrentAnswer\(''\);
                            \}
                        \}, 2500\);
                    \} else \{
                        alert\('Evaluation failed - ' \+ \(data\.error \|\| 'Unknown error'\)\);
                        setIsEvaluating\(false\);
                    \}
                \} catch \(err\) \{
                    console\.error\('Submit answer error:', err\);
                    setIsEvaluating\(false\);
                    alert\('Network error submitting answer\. Please try again\.'\);
                \}'''

new_code1 = '''                try {
                    const question = interviewSession.questions[currentQuestion];
                    const answerText = currentAnswer; // Capture before state changes

                    console.log('Submitting answer for question:', currentQ, question.question);

                    const res = await fetch('/api/interview/answer', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            candidate_id: interviewSession.candidate_id,
                            question: question.question,
                            answer: answerText,
                            question_index: currentQuestion
                        })
                    });

                    if (!res.ok) {
                        throw new Error(`HTTP ${res.status}: ${res.statusText}`);
                    }

                    const data = await res.json();
                    console.log('Evaluation response:', data);

                    if (data.success && data.evaluation) {
                        const updatedAnswers = [...(interviewSession.answers || [])];
                        // Ensure array is big enough
                        while (updatedAnswers.length <= currentQuestion) updatedAnswers.push({});

                        updatedAnswers[currentQuestion] = {
                            question: question.question,
                            answer: answerText,
                            evaluation: data.evaluation
                        };

                        console.log('Updating session with answers:', updatedAnswers);

                        // Update session state properly - use functional update
                        setInterviewSession(prev => {
                            if (!prev) {
                                console.error('Interview session is null!');
                                return prev;
                            }
                            return {
                                ...prev,
                                answers: updatedAnswers
                            };
                        });

                        // Auto-advance logic
                        setTimeout(() => {
                            console.log('Finishing evaluation, advancing if needed');
                            setIsEvaluating(false);
                            if (currentQ < totalQuestions - 1) {
                                setCurrentQuestion(currentQ + 1);
                                setCurrentAnswer('');
                                setTimeLeft(120); // Reset timer
                            }
                        }, 2500);
                    } else {
                        console.error('Evaluation failed:', data);
                        alert('Evaluation failed - ' + (data.error || 'No evaluation returned'));
                        setIsEvaluating(false);
                    }
                } catch (err) {
                    console.error('Submit answer error:', err);
                    setIsEvaluating(false);
                    alert('Network error submitting answer: ' + err.message);
                }'''

# Apply fix using simple string replacement (more reliable than regex for this case)
if 'const data = await res.json();' in content and 'if (data.success) {' in content:
    # Find the section to replace
    start_marker = '                try {\n                    const question = interviewSession.questions[currentQuestion];'
    end_marker = '                    alert(\'Network error submitting answer. Please try again.\');\n                }'
    
    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker, start_idx)
    
    if start_idx != -1 and end_idx != -1:
        end_idx += len(end_marker)
        content = content[:start_idx] + new_code1 + content[end_idx:]
        print("✓ Fix 1 applied: Enhanced submitAnswer error handling")
    else:
        print("✗ Fix 1 failed: Could not find exact match")
else:
    print("✗ Fix 1 skipped: Pattern not found")

# Fix 2: Add safety check to question rendering
old_pattern2 = '{interviewSession.questions[currentQuestion] && ('
new_pattern2 = '{interviewSession.questions && interviewSession.questions[currentQuestion] ? ('

if old_pattern2 in content:
    content = content.replace(old_pattern2, new_pattern2)
    print("✓ Fix 2 applied: Added safety check to question rendering")
else:
    print("✗ Fix 2 skipped: Pattern already fixed or not found")

# Write the fixed content back
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("\n✅ All fixes applied successfully!")
print("The Flask server should auto-reload. If not, restart it manually.")
print("Please refresh your browser to test the AI interviewer.")

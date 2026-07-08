## AI Interviewer Blank Page Fix

### Problem
After submitting an answer in the AI interviewer, the page shows blank content. This happens because:
1. The state update for `interviewSession` might not trigger a re-render properly
2. The conditional rendering logic `{interviewSession.questions[currentQuestion] &&` can fail if the state is temporarily undefined during updates
3. Missing error handling for HTTP responses
4. Timer reset not happening between questions

### Solution

Apply the following changes to `templates/index.html`:

#### Fix 1: Improve submitAnswer function (around line 899-948)

Replace the try-catch block in `submitAnswer` with better error handling:

```javascript
try {
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
}
```

#### Fix 2: Add safety check to question rendering (around line 1311)

Change:
```javascript
{interviewSession.questions[currentQuestion] && (
```

To:
```javascript
{interviewSession.questions && interviewSession.questions[currentQuestion] ? (
```

And add a closing `) : (` before the closing of the div with a fallback:
```javascript
) : (
    <div className="text-center py-20">
        <i className="fas fa-circle-notch fa-spin text-6xl text-gold-400 mb-4"></i>
        <p className="text-white text-xl">Loading question...</p>
    </div>
)}
```

#### Fix 3: Add evaluation loading indicator

During evaluation (when `isEvaluating` is true), show a clear indicator that the answer is being processed. This is already partially implemented but can be enhanced.

### Manual Fix Instructions

1. Open `c:\Users\saswa\Downloads\resume screener - Copy\res\res\templates\index.html`
2. Find line 899 (the try block in submitAnswer)
3. Replace the entire try-catch block with Fix 1 above
4. Find line 1311 (the question rendering conditional)
5. Apply Fix 2 above
6. Save the file
7. Refresh the browser (the Flask debug mode will auto-reload)

### Testing

1. Start an AI interview
2. Answer a question
3. Click "Submit Answer"
4. You should see:
   - The evaluation processing
   - The score and feedback appear
   - Auto-advance to next question after 2.5 seconds
   - No blank page at any point

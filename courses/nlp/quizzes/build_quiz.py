import re
import json
import markdown
import sys
import codecs

def parse_markdown_quiz(filepath):
    with codecs.open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
        
    # Remove the summary section at the end if it exists
    summary_split = re.split(r'## Summary of Answers', text)
    main_text = summary_split[0]
    
    # Split by the question title format `## Q1.1 ...`
    parts = re.split(r'\n## (Q\d+\.\d+.*?)(?=\n|$)', main_text)
    
    header_text = parts[0]
    titles = parts[1::2]
    contents = parts[2::2]
    
    quizzes = []
    
    for title, content in zip(titles, contents):
        q = {}
        q['title'] = title.strip()
        
        # Split until next `---` or end of part
        # Clean up `---\s*$` around the content
        content = re.sub(r'\n---\s*$', '', content.strip())
        
        # Separate Answer block
        ans_split = re.split(r'\n> \*\*Answer\*\*: ', '\n' + content)
        if len(ans_split) > 1:
            q_part = ans_split[0].strip()
            a_part = ans_split[1].strip()
        else:
            q_part = content
            a_part = ""
            
        q_lines = q_part.split('\n')
        prompt_lines = []
        options = []
        found_options = False
        correct_opt_id_from_checkbox = None
        
        for line in q_lines:
            s_line = line.strip()
            
            # Match A) Text
            m1 = re.match(r'^([A-Z])\)\s+(.*)$', s_line)
            if m1:
                options.append({"id": m1.group(1), "text": m1.group(2)})
                found_options = True
                continue
            
            # Match - [ ] Text or - [x] Text
            m2 = re.match(r'^- \[([ xX])\]\s+(.*)$', s_line)
            if m2:
                opt_id = chr(ord('A') + len(options))
                options.append({"id": opt_id, "text": m2.group(2)})
                if m2.group(1).lower() == 'x':
                    correct_opt_id_from_checkbox = opt_id
                found_options = True
                continue
                
            if not found_options:
                prompt_lines.append(line)
                
        q['prompt_html'] = markdown.markdown('\n'.join(prompt_lines).strip(), extensions=['fenced_code', 'tables'])
        q['options'] = options
        
        # Parse answer
        a_lines = a_part.split('\n')
        if a_lines and a_part.strip():
            raw_answer_line = a_lines[0].strip()
            q['raw_answer'] = raw_answer_line
            
            m_ans = re.match(r'^([A-Z])(?:\s|\(|$)', raw_answer_line)
            if m_ans:
                q['correct_id'] = m_ans.group(1)
            elif correct_opt_id_from_checkbox:
                q['correct_id'] = correct_opt_id_from_checkbox
            else:
                q['correct_id'] = None
                
            ex_lines = a_lines[1:]
            clean_ex = []
            for el in ex_lines:
                el = re.sub(r'^>\s?', '', el)
                clean_ex.append(el)
            
            q['explanation_html'] = markdown.markdown('\n'.join(clean_ex).strip(), extensions=['fenced_code', 'tables'])
        else:
            q['raw_answer'] = ""
            q['correct_id'] = None
            q['explanation_html'] = ""
            
        quizzes.append(q)
        
    return markdown.markdown(header_text, extensions=['fenced_code', 'tables']), quizzes

def build_html(output_file, header_html, quizzes):
    html_lines = []
    
    html_lines.append("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CST8507 NLP All Quizzes</title>
    
    <!-- MathJax for LaTeX rendering -->
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script>
    window.MathJax = {
      tex: {
        inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
        displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']],
        processEscapes: true
      },
      options: {
        skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre']
      }
    };
    </script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>

    <style>
        * { box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; padding: 20px; max-width: 800px; margin: auto; background-color: #f7f9fa; color: #333; line-height: 1.6; }
        .header-content { text-align: center; margin-bottom: 40px; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
        .quiz { background: white; padding: 30px; border-radius: 8px; margin-bottom: 30px; border-left: 5px solid #3498db; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
        h1, h2, h3 { color: #2c3e50; }
        h2 { border-bottom: 2px solid #ecf0f1; padding-bottom: 10px; margin-top: 0; font-size: 1.4em; }
        .prompt { margin-bottom: 20px; font-size: 1.1em; }
        .prompt blockquote { padding: 10px 15px; margin: 15px 0; border-left: 4px solid #3498db; background: #eaf2f8; color: #2980b9; border-radius: 0 4px 4px 0; font-size: 0.95em; }
        .options { display: flex; flex-direction: column; gap: 12px; margin-bottom: 25px; }
        .option { padding: 15px 20px; border: 2px solid #e0e6ed; border-radius: 8px; cursor: pointer; transition: all 0.2s ease; background: #fff; font-size: 1.05em; display: flex; align-items: baseline; }
        .option-id { font-weight: bold; margin-right: 15px; background: #ecf0f1; border-radius: 50%; width: 28px; height: 28px; display: inline-flex; align-items: center; justify-content: center; font-size: 0.9em; flex-shrink: 0; }
        .option:hover { border-color: #bdc3c7; background: #fdfdfd; transform: translateY(-1px); box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
        .option.selected { border-color: #3498db; background: #ebf5fb; }
        .option.selected .option-id { background: #3498db; color: white; }
        .option.correct { border-color: #2ecc71; background: #eafaf1; cursor: default; }
        .option.correct .option-id { background: #2ecc71; color: white; }
        .option.incorrect { border-color: #e74c3c; background: #fadbd8; cursor: default; }
        .option.incorrect .option-id { background: #e74c3c; color: white; }
        .btn { padding: 12px 24px; background: #3498db; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 16px; font-weight: bold; transition: all 0.2s; box-shadow: 0 2px 4px rgba(52, 152, 219, 0.3); }
        .btn:hover { background: #2980b9; box-shadow: 0 4px 6px rgba(41, 128, 185, 0.4); transform: translateY(-1px); }
        .btn:disabled { background: #95a5a6; cursor: not-allowed; box-shadow: none; transform: none; }
        .answer-block { margin-top: 25px; padding: 20px; border-radius: 8px; background: #fdfefe; display: none; border: 1px solid #dcdde1; box-shadow: inner 0 2px 4px rgba(0,0,0,0.02); }
        .answer-block.visible { display: block; animation: fadeIn 0.4s ease; }
        .answer-block p { margin-top: 0; }
        .answer-badge { display: inline-block; padding: 3px 8px; border-radius: 4px; background: #2ecc71; color: white; font-weight: bold; margin-top: 5px; }
        .explanation { margin-top: 15px; padding-top: 15px; border-top: 1px dashed #dcdde1; }
        .explanation blockquote { background: #fff3e0; border-left: 4px solid #f39c12; padding: 10px 15px; margin: 10px 0; color: #d35400; }
        code { background: #f1f2f6; padding: 3px 6px; border-radius: 4px; font-family: ui-monospace, SFMono-Regular, Consolas, "Liberation Mono", Menlo, monospace; font-size: 0.9em; color: #e84118; }
        pre { background: #2d3436; color: #f8f8f2; padding: 15px; border-radius: 6px; overflow-x: auto; }
        pre code { background: none; color: inherit; padding: 0; font-size: 0.85em; }
        table { width: 100%; border-collapse: collapse; margin: 15px 0; }
        th, td { padding: 10px; border: 1px solid #dfe6e9; text-align: left; }
        th { background: #f1f2f6; }
        
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
    </style>
</head>
<body>""")

    html_lines.append(f'<div class="header-content">{header_html}</div>')
    
    for i, q in enumerate(quizzes):
        html_lines.append(f'<div class="quiz" id="q-{i}">')
        html_lines.append(f'<h2>{q["title"]}</h2>')
        html_lines.append(f'<div class="prompt">{q["prompt_html"]}</div>')
        
        if q['options']:
            html_lines.append(f'<div class="options" id="opts-{i}">')
            for opt in q['options']:
                # The onclick will pass 'this' and opt.id to JS
                html_lines.append(f'<div class="option" id="opt-{i}-{opt["id"]}" data-id="{opt["id"]}" onclick="selectOption({i}, \'{opt["id"]}\')">')
                html_lines.append(f'<span class="option-id">{opt["id"]}</span> <span>{markdown.markdown(opt["text"]).replace("<p>","").replace("</p>","")}</span>')
                html_lines.append('</div>')
            html_lines.append('</div>')
            
        c_id = q['correct_id'] if q['correct_id'] else "None"
        raw_ans = q['raw_answer'].replace("'", "\\'") # escape quotes
        
        btn_text = "Submit" if q['options'] else "Show Answer"
        html_lines.append(f'<button class="btn" id="btn-{i}" onclick="checkAnswer({i}, \'{c_id}\')">{btn_text}</button>')
        
        html_lines.append(f'<div class="answer-block" id="ans-{i}">')
        html_lines.append(f'<p><strong>Correct Answer:</strong> <span class="answer-badge">{q["raw_answer"]}</span></p>')
        html_lines.append(f'<div class="explanation">{q["explanation_html"]}</div>')
        html_lines.append('</div>')
        
        html_lines.append('</div>')
        
    html_lines.append("""
    <script>
        function selectOption(qIndex, optId) {
            const btn = document.getElementById(`btn-${qIndex}`);
            if (btn.disabled) return;
            
            const opts = document.querySelectorAll(`#opts-${qIndex} .option`);
            opts.forEach(o => o.classList.remove('selected'));
            
            const clicked = document.getElementById(`opt-${qIndex}-${optId}`);
            clicked.classList.add('selected');
        }

        function checkAnswer(qIndex, correctId) {
            const btn = document.getElementById(`btn-${qIndex}`);
            const ansBlock = document.getElementById(`ans-${qIndex}`);
            
            btn.disabled = true;
            ansBlock.classList.add('visible');
            
            if (correctId && correctId !== 'None') {
                const opts = document.querySelectorAll(`#opts-${qIndex} .option`);
                opts.forEach(o => {
                    const id = o.dataset.id;
                    if (id === correctId) {
                        o.classList.add('correct');
                    } else if (o.classList.contains('selected')) {
                        o.classList.add('incorrect');
                    }
                });
            }
        }
    </script>
</body>
</html>
""")

    with codecs.open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(html_lines))

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python build_quiz.py input.md output.html")
        sys.exit(1)
        
    header, quizzes = parse_markdown_quiz(sys.argv[1])
    build_html(sys.argv[2], header, quizzes)
    print(f"Successfully generated {sys.argv[2]} with {len(quizzes)} quizzes.")

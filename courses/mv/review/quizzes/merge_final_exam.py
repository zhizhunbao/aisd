import json

# Merge part1 (MCQ) and part2 (Fill + Short) into final_exam_quiz.json
parts = []
for f in ['final_exam_part1.json', 'final_exam_part2.json']:
    with open(f, 'r', encoding='utf-8') as fh:
        parts.extend(json.load(fh))

with open('final_exam_quiz.json', 'w', encoding='utf-8') as fh:
    json.dump(parts, fh, ensure_ascii=False, indent=2)

print(f"Merged {len(parts)} questions into final_exam_quiz.json")

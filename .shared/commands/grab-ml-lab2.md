---
description: Grab Machine Learning Lab 2 data from Brightspace
---

1. Navigate to the scraper directory

```bash
cd .skills/learning-brightspace_scraper/scripts
```

// turbo 2. Run the scraper for ML Course (846088) and Module "Lab 2"

```bash
uv run python run.py --course 846088 --module "Lab 2"
```

3. Review the downloaded content in the `data/ml/` directory.

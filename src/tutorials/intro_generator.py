import json
import os

class IntroGenerator:
    def __init__(self):
        self.steps = []

    def add_step(self, element: str, title: str, intro: str, position: str = "bottom"):
        """
        Add a step for the Intro.js tour.
        - element: CSS selector for the target element.
        - title: Title to display.
        - intro: The description text.
        - position: The tooltip position.
        """
        step = {
            "element": element,
            "title": title,
            "intro": intro,
            "position": position
        }
        self.steps.append(step)

    async def inject_introjs(self, page):
        """
        Inject Intro.js CSS and JS into the page if not already loaded.
        """
        is_loaded = await page.evaluate("typeof window.introJs !== 'undefined'")
        if not is_loaded:
            await page.add_style_tag(url="https://unpkg.com/intro.js/minified/introjs.min.css")
            await page.add_script_tag(url="https://unpkg.com/intro.js/minified/intro.min.js")
            await page.wait_for_timeout(1000)

    async def start_tour(self, page, step_delay: int = 3000):
        """
        Start the Intro.js tour automatically, advancing steps after a fixed delay.
        - step_delay: delay in milliseconds before advancing to the next step.
        """
        await self.inject_introjs(page)
        steps_json = json.dumps(self.steps)
        js_code = f"""
        (function() {{
            var tour = introJs();
            tour.setOptions({{
                steps: {steps_json},
                exitOnOverlayClick: false,
                showBullets: false,
                showStepNumbers: false,
                disableInteraction: true
            }});
            tour.start();

            // Auto-advance each step after {step_delay} ms
            function autoNext() {{
                setTimeout(function() {{
                    if (tour._currentStep < tour._options.steps.length - 1) {{
                        tour.nextStep();
                        autoNext();
                    }} else {{
                        tour.exit();
                    }}
                }}, {step_delay});
            }}
            autoNext();
        }})();
        """
        await page.evaluate(js_code)

    def save_tutorial(self, output_path: str):
        """
        Save the configured tutorial steps to a JSON file.
        """
        os.makedirs(output_path, exist_ok=True)
        file_path = os.path.join(output_path, "tutorial.json")
        with open(file_path, "w") as f:
            json.dump(self.steps, f, indent=2)

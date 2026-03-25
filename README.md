# Getting Started with GitHub Copilot

_Get started using GitHub Copilot in less than an hour._

## Welcome

- **Who is this for**: Developers at any experience level looking to accelerate their code workflow.
- **What you'll learn**: The different ways to interact with Copilot to explain, write, plan, and develop code.
- **What you'll build**: You will guide Copilot to update Mergington High School's extracurricular activities website.
- **Prerequisites**:
  - Skills exercise: [Introduction to GitHub](https://github.com/skills/introduction-to-github)
  - Familiarity with [VS Code](https://code.visualstudio.com/)
  - Basic coding principles
- **How long**: This exercise takes less than one hour to complete.

In this exercise, you will:

1. Use a preconfigured Codespace to run VS Code in your browser.
1. Learn different interaction options to develop and plan with GitHub Copilot.
1. Use Copilot to summarize and review your pull request.

### How to start this exercise

Simply copy the exercise to your account, then give your favorite Octocat (Mona) **about 20 seconds** to prepare the first lesson, then **refresh the page**.

[![](https://img.shields.io/badge/Copy%20Exercise-%E2%86%92-1f883d?style=for-the-badge&logo=github&labelColor=197935)](https://github.com/new?template_owner=skills&template_name=getting-started-with-github-copilot&owner=%40me&name=skills-getting-started-with-github-copilot&description=Exercise:+Get+started+using+GitHub+Copilot&visibility=public)

<details>
<summary>Having trouble? 🤷</summary><br/>

When copying the exercise, we recommend the following settings:

- For owner, choose your personal account or an organization to host the repository.

- We recommend creating a public repository, since private repositories will use Actions minutes.
   
If the exercise isn't ready in 20 seconds, please check the [Actions](../../actions) tab.

- Check to see if a job is running. Sometimes it simply takes a bit longer.

- If the page shows a failed job, please submit an issue. Nice, you found a bug! 🐛

</details>

---

## Desktop Recorder

This repository also ships a **Desktop Graphics Application Recorder & Player** — a standalone executable that records and replays every mouse and keyboard interaction with any desktop application.

### Where to find the compiled executable

#### Option 1 — Download a pre-built binary from GitHub Actions (recommended)

Every push to this repository automatically triggers the **"Build Desktop Recorder Executable"** workflow, which compiles the tool for Linux, macOS, and Windows and uploads the result as a downloadable artifact.

To get the binary:

1. Open the [**Actions**](../../actions/workflows/build-exe.yml) tab of this repository.
2. Click the most recent **Build Desktop Recorder Executable** run marked ✅.
3. Scroll to the **Artifacts** section at the bottom of the run page.
4. Download the zip for your operating system:

   | Artifact name | Platform |
   |---|---|
   | `desktop_recorder` | Linux |
   | `desktop_recorder.exe` | Windows |
   | `desktop_recorder-macos` | macOS |

5. Unzip the download and run the binary directly — no Python installation required.

#### Option 2 — Build it yourself locally

```bash
# 1. Install Python 3.12+ and the project dependencies
pip install -r requirements.txt

# 2. Run the build script
python build.py

# 3. The executable is placed in dist/
#    Linux / macOS:  dist/desktop_recorder
#    Windows:        dist/desktop_recorder.exe
```

### Quick-start

```bash
# Record your interactions with any desktop application (press Ctrl+C to stop)
./dist/desktop_recorder record -o my_session.json

# Replay the recording at 1× speed
./dist/desktop_recorder play -i my_session.json

# Replay at 2× speed with event tracing
./dist/desktop_recorder play -i my_session.json --speed 2.0 --verbose

# Inspect the contents of a session file without replaying
./dist/desktop_recorder list -i my_session.json --events
```

---

&copy; 2025 GitHub &bull; [Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/code_of_conduct.md) &bull; [MIT License](https://gh.io/mit)
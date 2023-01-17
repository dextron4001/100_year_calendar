# Variables
APP_NAME = my-dash-app
BUILD_DIR = build
GITHUB_PAGES_BRANCH = gh-pages

# Convert the app to a static website
static:
	# Create the build directory
	mkdir -p $(BUILD_DIR)
	# Convert the app to a static website
	python -m dash_renderer.tool.renderer $(APP_NAME) $(BUILD_DIR)

# Deploy to GitHub Pages
deploy: static
	# Checkout the GitHub Pages branch
	git checkout $(GITHUB_PAGES_BRANCH)
	# Add and commit the build files
	git add -f $(BUILD_DIR)/
	git commit -m "Deploy to GitHub Pages"
	# Push the branch to GitHub
	git push origin $(GITHUB_PAGES_BRANCH) -f
	# Checkout the previous branch
	git checkout -
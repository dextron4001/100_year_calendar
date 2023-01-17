# Variables
APP_NAME = app.py
BUILD_DIR = https://github.com/dextron4001/100_year_calendar.git
GITHUB_PAGES_BRANCH = main

html:
	export DEBUG=False && python3 app.py &
	sleep 60
	wget -r http://127.0.0.1:8050/ 
	wget -r http://127.0.0.1:8050/_dash-layout 
	wget -r http://127.0.0.1:8050/_dash-dependencies
	sed -i 's/_dash-layout/_dash-layout.json/g' 127.0.0.1:8050/_dash-component-suites/dash_renderer/*.js 
	sed -i 's/_dash-dependencies/_dash-dependencies.json/g' 127.0.0.1:8050/_dash-component-suites/dash_renderer/*.js




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
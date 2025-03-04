# 🌲 Socioeconomic Development in South America: Agriculture, forestry, and fishing & GDP Trends📊

# Elise Reynolds
Community Action Computing (Spring 2025)

Professor: Mike Ryu

# Thesis Statement: 
The economic development in South America is deeply intertwined with the agricultural sector, which has been historically a key driven of GDP. This project explores how agriculture, forestry, and fishing contribute to national economies across South America. 

# Features:
- **Choropleth Map:** Displays the selected socioeconomic indicator (depends on which the user chooses - 2 options) for South American countries 
- **Line Chart:** Shows the trends of arg value added (% of gdp) and overall GDP (in current US$) over time for different countries 
- **Bar Charts:** Compare 2 selected countries at a times' arg value added (% of GDP) across years 
- **Interactive Components:** users can select which dataset they want to see, adjust the year range, and choose specific countries for comparison.

# Context for Data Visualization
Arg, forestry, and fishing play a crucial role in the economies of South American countries, particularly Brazil. As one of the largest agricultural producers & exporters, Brazil relies alot on these industries of economic growth, employment, and trade. However, this economic dependency also brings significant environmental challenges, such as deforestation in the Amazon and concerns about sustainable land use. 
This visualization explores the % of GDP derived from arg, forestry, and fishing across South America. By analyzing these trends, the visualization aims to highlight regional patterns and prompt possible topics about the economic sustainability, diversification, and the role of arg in long-term growth strategies. 

# Dataset Description & Selection 
The dataset used in my project comes from **World Bank Open Data**, in specific: 
1. **Agriculture, Forestry, and Fishing Value Added (% of GDP)** - NV.AGR.TOTL.ZS
2. **Total GDP (current US$)** - NY.GDP.MKTP.CD

I think that these indicators effectively highlight economic shifts over time. The first dataset reveals the relative dependence of each country on arg, while the second provides context by showing the total economic output. 

# Strategies from "Storytelling with Data" (SwD)
To ensure the effectiveness of this visualization, I will employ several key strategies from this book! 

1. **Showing key trends & insights:** 
    - the map uses a color gradiant to emphasize the differences in countries with higher & lower reliance on arg (even tho alot of them are similar-ish numbers, thats also important data to show!)
    - the time series line graph is meant to emphasize the historical trends, and allow users to look comparatively at how the % of arg looks next to total gdp
2. **Interactivity to Engage the Audience:** 
    - the drop down menu allows users to switch between economic indicators, first getting a handle on what each one is overall (not dynamically with anything else)
3. **Simplify:** 
    - I like how the dark mode emphasizes the graphs themselves, and draws your attention to them! 
    - I also like how their is consistent colorings 
4. **Comparisons across countries & time:**
    - my hope was that the side by side views will help the user see the differences of the two data (or similarities)
    - the year range slider will make it easier to track the historical changes

# Data Sources:
- https://data.worldbank.org/indicator/NV.AGR.TOTL.ZS
- https://data.worldbank.org/indicator/NY.GDP.MKTP.CD?view=chart
- https://www.ers.usda.gov/amber-waves/2022/september/brazil-s-momentum-as-a-global-agricultural-supplier-faces-headwinds

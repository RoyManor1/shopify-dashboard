import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import morethemes as mt
import os
import re
import numpy as np
import matplotlib.ticker as mtick  # For formatting numbers with commas

###############################################################################
# 1. SET THE THEME
###############################################################################
mt.set_theme("wsj")  # Using MoreThemes for a professional WSJ-inspired look.

###############################################################################
# 2. LOAD DATA FROM DESKTOP
###############################################################################
desktop_path = os.path.expanduser("~/Desktop")
csv_file = os.path.join(desktop_path, "Shopifycleaned_US.csv")

try:
    df = pd.read_csv(csv_file)
except FileNotFoundError:
    print("Error: 'Shopifycleaned_US.csv' was not found on your Desktop.")
    exit()
except Exception as e:
    print(f"Error reading CSV: {e}")
    exit()

###############################################################################
# 3. PROCESS DATE & STATE DATA
###############################################################################
# Convert the "created" column to datetime (format dd/mm/yyyy)
if "created" in df.columns:
    df["created_dt"] = pd.to_datetime(df["created"], dayfirst=True, errors="coerce")
else:
    print("Warning: 'created' column not found. Line chart may be skipped.")

# Identify state column
if "pm_state" in df.columns:
    state_col = "pm_state"
elif "state" in df.columns:
    state_col = "state"
else:
    print("Error: No state column found (neither 'pm_state' nor 'state').")
    exit()

###############################################################################
# 4. HELPER FUNCTIONS
###############################################################################
def parse_tokens(text):
    """Splits a string by colon, comma, or semicolon and returns stripped tokens."""
    if pd.isna(text):
        return []
    return [t.strip() for t in re.split(r'[:,;]', text) if t.strip()]

###############################################################################
# 5. TOP 10 MARKETING APPS CHART
###############################################################################
marketing_apps = [
    "Klaviyo",
    "Omnisend",
    "Yotpo",
    "Judge.me",
    "Loox",
    "Rebuy",
    "Privy",
    "Pop Convert",
    "UpPromote",
    "Algolia",
    "PushOwl/Brevo",  # counts "pushowl" or "brevo" in the row
    "Stamped.io",
    "Mailchimp"
]

if "installed_apps_names" in df.columns:
    marketing_counts = {app: 0 for app in marketing_apps}
    for row in df["installed_apps_names"].dropna():
        row_lower = row.lower()
        for app in marketing_apps:
            if app == "PushOwl/Brevo":
                if "pushowl" in row_lower or "brevo" in row_lower:
                    marketing_counts[app] += 1
            else:
                if app.lower() in row_lower:
                    marketing_counts[app] += 1

    marketing_series = pd.Series(marketing_counts).sort_values(ascending=False)
    top_marketing = marketing_series.head(10)
    
    fig1, ax1 = plt.subplots(figsize=(8, 6))
    sns.barplot(x=top_marketing.values, y=top_marketing.index, ax=ax1, palette="deep")
    ax1.set_title("Top 10 Marketing Apps")
    ax1.set_xlabel("Count")
    ax1.set_ylabel("Marketing App")
    # Format the x-axis numbers with commas
    ax1.xaxis.set_major_formatter(mtick.StrMethodFormatter('{x:,.0f}'))
    
    plt.tight_layout()
    plt.show()
else:
    print("Column 'installed_apps_names' not found; skipping Marketing Apps chart.")

###############################################################################
# 6. PIE CHART: STORE DISTRIBUTION BY STATE (Main vs. Others, max Others = 14%)
###############################################################################
if state_col in df.columns:
    state_counts = df[state_col].value_counts()
    total = state_counts.sum()
    
    main_states = state_counts[state_counts / total >= 0.02].copy()
    others_sum = state_counts[state_counts / total < 0.02].sum()
    
    max_others = 0.14 * total
    final_others = min(others_sum, max_others)
    if final_others > 0:
        main_states["Others"] = final_others

    fig2, ax2 = plt.subplots(figsize=(6, 6))
    ax2.pie(main_states.values, labels=main_states.index, autopct="%1.1f%%",
            startangle=140, wedgeprops={"edgecolor": "white"}, textprops={"fontsize":9})
    ax2.set_title("Store Distribution by State")
    plt.tight_layout()
    plt.show()
else:
    print(f"Column '{state_col}' not found; skipping store distribution pie chart.")

###############################################################################
# 7. SCATTER PLOT: ESTIMATED MONTHLY PAGEVIEWS VS. SALES
###############################################################################
if "estimated_monthly_pageviews" in df.columns and "estimated_monthly_sales" in df.columns:
    # Cap extreme values at the 99th percentile to reduce scale distortion
    sales_cap = df["estimated_monthly_sales"].quantile(0.99)
    views_cap = df["estimated_monthly_pageviews"].quantile(0.99)
    df_scatter = df[(df["estimated_monthly_sales"] < sales_cap) &
                    (df["estimated_monthly_pageviews"] < views_cap)]
    
    fig3, ax3 = plt.subplots(figsize=(8, 6))
    sns.scatterplot(data=df_scatter,
                    x="estimated_monthly_pageviews",
                    y="estimated_monthly_sales",
                    ax=ax3, alpha=0.7, color="navy")
    sns.regplot(data=df_scatter,
                x="estimated_monthly_pageviews",
                y="estimated_monthly_sales",
                ax=ax3,
                scatter=False,
                color="orange",
                lowess=True)
    # Combine the main title and the context text in a multi-line string
    title_text = (
        "Monthly Pageviews vs. Monthly Sales (Capped at 99th Percentile)\n"
        "Each dot represents one Shopify store. The orange line shows the average trend between traffic and revenue."
    )
    ax3.set_title(title_text)
    ax3.set_xlabel("Estimated Monthly Pageviews")
    ax3.set_ylabel("Estimated Monthly Sales")
    
    # Format x and y axes with commas/$ sign
    ax3.xaxis.set_major_formatter(mtick.StrMethodFormatter('{x:,.0f}'))
    ax3.yaxis.set_major_formatter(mtick.StrMethodFormatter('${x:,.0f}'))
    
    plt.tight_layout()
    plt.show()
else:
    print("Columns for pageviews or sales not found; skipping scatter plot.")

###############################################################################
# 8. LINE CHART: MEDIAN MONTHLY SALES BY STORE CREATION MONTH (3-Month Average)
#       (After Removing Top 1% Outliers)
###############################################################################
if "created_dt" in df.columns and "estimated_monthly_sales" in df.columns:
    sales_cap_line = df["estimated_monthly_sales"].quantile(0.99)
    df_line = df[df["estimated_monthly_sales"] < sales_cap_line].copy()
    
    df_line["year_month"] = df_line["created_dt"].dt.to_period("M")
    grouped = df_line.groupby("year_month")["estimated_monthly_sales"].median().reset_index()
    grouped["year_month_dt"] = grouped["year_month"].dt.to_timestamp()
    grouped["rolling_median"] = grouped["estimated_monthly_sales"].rolling(window=3, min_periods=1).mean()
    
    fig4, ax4 = plt.subplots(figsize=(10, 4))
    sns.lineplot(data=grouped, x="year_month_dt", y="rolling_median", marker="o", ax=ax4)
    ax4.set_title("3-Month Rolling Median Sales by Store Creation Month\n(Top 1% Outliers Removed)")
    ax4.set_xlabel("Store Creation Month")
    ax4.set_ylabel("3-Month Rolling Median Sales")
    
    ax4.yaxis.set_major_formatter(mtick.StrMethodFormatter('${x:,.0f}'))
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
else:
    print("Missing 'created_dt' or 'estimated_monthly_sales'; skipping line chart.")

###############################################################################
# 9. BAR CHART: TOP 10 TECHNOLOGIES
###############################################################################
if "technologies" in df.columns:
    all_techs = df["technologies"].dropna().apply(parse_tokens).explode()
    top_techs = all_techs.value_counts().head(10)
    
    fig5, ax5 = plt.subplots(figsize=(8, 6))
    sns.barplot(x=top_techs.values, y=top_techs.index, ax=ax5, palette="rocket")
    ax5.set_title("Top 10 Technologies")
    ax5.set_xlabel("Count")
    ax5.set_ylabel("Technology")
    # Format the x-axis with commas
    ax5.xaxis.set_major_formatter(mtick.StrMethodFormatter('{x:,.0f}'))
    plt.tight_layout()
    plt.show()
else:
    print("Column 'technologies' not found; skipping Top 10 Technologies chart.")

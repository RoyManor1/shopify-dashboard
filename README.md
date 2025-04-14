# 🛍️ Shopify Dashboard

This project visualizes trends from a dataset of **1 million Shopify stores**, using Python, Seaborn, and MoreThemes.  
It explores how traffic, technology stacks, and store creation timelines affect performance across the platform.

---

## 🔍 Key Insights

- 📉 **Median monthly sales** of new stores have **declined sharply since 2020**, reflecting increased competition and saturation.
- 🛒 **Klaviyo** dominates the marketing app landscape, with significant adoption across stores.
- 📈 More pageviews typically lead to higher sales — but **conversion rates vary significantly**, even among stores with similar traffic levels.
- 🧠 Stores created earlier tend to outperform newer stores in revenue.

---

## 📊 Visual Highlights

---

### 1️⃣ Median Monthly Sales Over Time (2006–2024)

This line chart shows the **3-month rolling median monthly sales** based on store creation date.  
It excludes the top 1% of outliers to focus on typical store performance.

📉 Key Trend: Newer stores earn significantly less than earlier ones.

![Line Chart](creationstore.png)

---

### 2️⃣ Pageviews vs. Monthly Sales (Performance Scatter)


📈 Some stores with similar traffic convert far better than others, highlighting the gap in optimization and business models.

![Scatter Plot](PageViewVSsales.png)

---

### 3️⃣ Store Distribution by State

Displays the percentage of stores from each U.S. state.  

🌍 California, Florida, and Texas lead in store count.

![State Distribution](StateDistrubution.png)

---

### 4️⃣ Top 10 Marketing Apps

This bar chart shows the top marketing tools installed by Shopify stores.  

🔥 Klaviyo dominates the field with 92,802 clients, followed closely by Judge.me and Mailchimp.

![Top 10 Apps](Top10Apps.png)

---

### 5️⃣ Top 10 Technologies Used by Shopify Stores

Ranks the most common technologies in Shopify stacks — including payment processors, analytics, and CDNs.

⚙️ Cloudflare and Shop Pay are among the most widely adopted tools.

![Top 10 Technologies](Top10Technologies.png)

---

## 🧪 Tools Used

- **Python 3**
- **Pandas**, **Matplotlib**, **Seaborn**, **MoreThemes**
- Dataset: Publicly available scraped data from StoreLeads.io

---


   pip install pandas matplotlib seaborn morethemes

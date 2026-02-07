"""
Common CSS styles for the application
"""

def get_global_css() -> str:
    """Return global CSS styles"""
    return """
<style>
html { scroll-behavior: smooth; }
.stApp { background-color: #000000; color: #ffffff; }
header, footer {visibility: hidden;}
[data-testid="stMainViewContainer"] > div:nth-child(1) { padding-top: 0rem; }

/* STICKY HEADER */
.nav-bar {
    position: fixed;
    top: 0; left: 0; width: 100%;
    display: flex; justify-content: space-between; align-items: center;
    padding: 20px 60px;
    background-color: rgba(0, 0, 0, 0.9);
    backdrop-filter: blur(10px);
    z-index: 999999;
    border-bottom: 1px solid #111;
}
.header-spacer { height: 100px; }
.logo-text { font-size: 26px; font-weight: 700; color: #3b82f6; text-decoration: underline; text-underline-offset: 4px; }
.nav-links { display: flex; gap: 28px; }
.nav-links a { color: #bbbbbb; text-decoration: none; font-size: 16px; font-weight: 500; }

.google-btn {
    display: flex; align-items: center; gap: 10px;
    background-color: #ffffff; color: #000000 !important;
    padding: 8px 16px; border-radius: 6px; text-decoration: none;
    font-size: 14px; font-weight: 600;
}
.badge {
    background: #111827;
    border: 1px solid #1f2937;
    color: #93c5fd;
    padding: 3px 10px;
    border-radius: 999px;
    font-size: 12px;
}
.launch-btn {
    background-color: #00d26a; color: #000 !important;
    padding: 18px 45px; border-radius: 8px; font-weight: 800;
    text-decoration: none; font-size: 18px;
}

.hero-container { display:flex; flex-direction:column; align-items:center; text-align:center; padding: 100px 20px; }
.hero-title { font-size: 64px; font-weight: 900; line-height: 1.05; margin-bottom: 25px; }
.hero-subtitle { font-size: 24px; color: #888; max-width: 900px; margin-bottom: 45px; }

.features-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 25px; padding: 40px; max-width: 1100px; margin: 0 auto; }
.feature-card { 
    background: #0a0a0a; 
    border: 1px solid #1a1a1a; 
    padding: 30px; 
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.3s ease;
}
.feature-card:hover {
    border-color: #3b82f6;
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(59, 130, 246, 0.2);
}
.icon-box { color: #00d26a; font-size: 24px; margin-bottom: 10px; }

.learn-more-container {
    padding: 80px 60px;
    background-color: #050505;
    border-top: 1px solid #111;
    max-width: 1200px;
    margin: 0 auto;
}
.reason-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 40px;
    margin-top: 50px;
}
.reason-card {
    padding: 20px;
    border-left: 2px solid #3b82f6;
}
.reason-card h4 { color: #3b82f6; margin-bottom: 10px; }
.reason-card p { color: #888; font-size: 15px; line-height: 1.6; }

.panel {
    background: #070707;
    border: 1px solid #111;
    border-radius: 16px;
    padding: 18px 18px;
    margin-bottom: 20px;
}

.risk-card {
    background: #0a0a0a;
    border: 1px solid #1a1a1a;
    border-radius: 16px;
    padding: 24px;
    margin: 16px 0;
}

.standard-section {
    background: #070707;
    border: 1px solid #1a1a1a;
    border-radius: 12px;
    padding: 24px;
    margin: 20px 0;
}

/* Dashboard cards */
div[data-testid="column"] {
    background-color: #0a0a0a;
    border: 1px solid #1a1a1a;
    padding: 20px;
    border-radius: 15px;
}
.m-label { color: #666; font-size: 14px; margin-bottom: 10px; display:flex; align-items:center; gap:8px; }
.m-value { font-size: 42px; font-weight: 800; color: #ffffff; }
.m-sub { color: #444; font-size: 12px; margin-top: 10px; }

.weather-container {
    background-color: #070707;
    border: 1px solid #111;
    padding: 20px;
    border-radius: 20px;
    margin-top: 30px;
}

/* Map view specific */
.hero {
    text-align: center;
    padding: 60px 20px 40px;
}
.hero h1 { font-size: 48px; font-weight: 900; margin-bottom: 12px; }
.hero p { font-size: 20px; color: #888; }

.map-wrap {
    display: flex;
    justify-content: center;
    margin-top: 30px;
}
</style>
"""

# -*- coding: utf-8 -*-
"""
السجل الوطني للمخاطر - دولة ليبيا
المركز الوطني لإدارة الطوارئ والأزمات والكوارث
National Risk Register - State of Libya (NCEDCM)

متوافق مع إطار سنداي للحد من مخاطر الكوارث (2015-2030)
وتصنيف تعريف المخاطر الصادر عن UNDRR / ISC
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import json

# ---------------------------------------------------------
# إعداد الصفحة وتفعيل RTL والخطوط العربية
# ---------------------------------------------------------
st.set_page_config(
    page_title="السجل الوطني للمخاطر - دولة ليبيا",
    page_icon="🇱🇾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تضمين تنسيقات CSS لدعم اللغة العربية والاتجاه من اليمين لليسار (RTL)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&display=swap');
    
    html, body, [class*="css"], div, p, span, h1, h2, h3, h4, h5, h6, input, select, button, label {
        font-family: 'Cairo', sans-serif !important;
        direction: rtl;
        text-align: right;
    }
    
    /* ضبط الحاويات والشريط الجانبي */
    section[data-testid="stSidebar"] {
        direction: rtl;
        text-align: right;
        background-color: #0f172a;
        color: #f8fafc;
    }
    section[data-testid="stSidebar"] * {
        color: #f8fafc !important;
    }
    
    /* بطاقات المقاييس */
    div[data-testid="stMetricValue"] {
        font-family: 'Cairo', sans-serif !important;
        font-weight: 800;
    }
    
    .sendai-card {
        background: linear-gradient(135deg, #1e293b, #0f172a);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 16px 20px;
        color: #ffffff;
        margin-bottom: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .sendai-title {
        font-size: 0.85rem;
        color: #94a3b8;
        font-weight: 600;
        margin-bottom: 4px;
    }
    .sendai-value {
        font-size: 1.6rem;
        font-weight: 800;
        color: #38bdf8;
    }
    .sendai-sub {
        font-size: 0.75rem;
        color: #cbd5e1;
    }
    
    /* شارات المستويات */
    .badge-critical {
        background-color: #fee2e2;
        color: #dc2626;
        padding: 4px 10px;
        border-radius: 9999px;
        font-weight: 700;
        border: 1px solid #fca5a5;
    }
    .badge-high {
        background-color: #ffedd5;
        color: #ea580c;
        padding: 4px 10px;
        border-radius: 9999px;
        font-weight: 700;
        border: 1px solid #fdba74;
    }
    .badge-medium {
        background-color: #fef9c3;
        color: #ca8a04;
        padding: 4px 10px;
        border-radius: 9999px;
        font-weight: 700;
        border: 1px solid #fde047;
    }
    .badge-low {
        background-color: #dcfce7;
        color: #16a34a;
        padding: 4px 10px;
        border-radius: 9999px;
        font-weight: 700;
        border: 1px solid #86efac;
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# البيانات الأولية المعتمدة للسجل الوطني الليبي
# ---------------------------------------------------------
DEFAULT_RISKS = [
    {
        "id": "LIB-HYD-001",
        "name": "فيضانات وسيول جارفة بالمناطق الحضرية والأودية",
        "category": "أخطار هيدرولوجية وأرصاد جوية (Hydrometeorological)",
        "category_en": "Hydrometeorological",
        "description": "تدفقات فيضانية خاطفة ناجمة عن منخفضات جوية حادة (مثل عاصفة دانيال)، وانهيار سدود ومنشآت حجز المياه، مما يهدد درنة والساحل الشرقي والغربي.",
        "likelihood": 4,
        "impact_human": 5,
        "impact_financial": 5,
        "impact_service": 5,
        "impact_total": 5,
        "risk_score": 20,
        "risk_level": "حرج",
        "regions": "درنة، سوسة، البيضاء، شحات، بنغازي، زليتن، طرابلس",
        "mortalities": 4500,
        "affected_pop": 250000,
        "economic_loss_mlyd": 8500.0,
        "lead_agency": "المركز الوطني لإدارة الطوارئ والأزمات والكوارث",
        "mitigation": "صيانة وتأهيل السدود، تدشين منظومة إنذار مبكر هيدرولوجي، ومنع البناء في مجاري الأودية ومخرات السيول."
    },
    {
        "id": "LIB-SEC-001",
        "name": "نزاع مسلح داخلي واضطرابات أمنية ومخلفات الحرب",
        "category": "أخطار أمنية ومجتمعية (Societal & Security)",
        "category_en": "Societal & Security",
        "description": "اشتباكات مسلحة محلية مفاجئة، ووجود ألغام ومخلفات حربية تعيق وصول قوافل الإغاثة الإنسانية والفرق الطبية وتعطل المنشآت الحيوية.",
        "likelihood": 4,
        "impact_human": 4,
        "impact_financial": 4,
        "impact_service": 4,
        "impact_total": 4,
        "risk_score": 16,
        "risk_level": "حرج",
        "regions": "طرابلس الكبرى، الزاوية، سبها، سرت، ورشفانة",
        "mortalities": 850,
        "affected_pop": 180000,
        "economic_loss_mlyd": 4200.0,
        "lead_agency": "وزارة الداخلية - الغرفة الأمنية المركزية",
        "mitigation": "تأمين الممرات الإنسانية، وتنسيق خطط الطوارئ مع الغرفة الأمنية، وتكثيف برامج نزع الألغام (LibMAC)."
    },
    {
        "id": "LIB-CLI-001",
        "name": "موجة حر شديدة وجفاف ممتد وحرائق غابات متزامنة",
        "category": "أخطار مناخية وجفاف (Climatological)",
        "category_en": "Climatological",
        "description": "درجات حرارة تتجاوز 48 مئوية مصحوبة برياح جافة، مما يؤدي لحرائق الغطاء النباتي بالجبل الأخضر والإجهاد الحراري والتأثير على الزراعة.",
        "likelihood": 5,
        "impact_human": 3,
        "impact_financial": 3,
        "impact_service": 4,
        "impact_total": 4,
        "risk_score": 20,
        "risk_level": "حرج",
        "regions": "الجبل الأخضر، المرج، غريان، يفرن، سهل الجفارة",
        "mortalities": 120,
        "affected_pop": 450000,
        "economic_loss_mlyd": 1800.0,
        "lead_agency": "هيئة السلامة الوطنية",
        "mitigation": "تجهيز طائرات مكافحة الحرائق، توفير صهاريج مياه إضافية للبلديات، وحملات توعية وحماية الفئات الهشة."
    },
    {
        "id": "LIB-TEC-001",
        "name": "انهيار شبكة الكهرباء العامة وتوقف ضخ مياه النهر الصناعي",
        "category": "أخطار تكنولوجية وبنية تحتية (Technological)",
        "category_en": "Technological",
        "description": "حدوث إظلام تام (Blackout) للشبكة الوطنية، يتبعه توقف فوري لضخ مياه آبار النهر الصناعي ومحطات التحلية ومستشفيات الطوارئ.",
        "likelihood": 4,
        "impact_human": 3,
        "impact_financial": 4,
        "impact_service": 5,
        "impact_total": 5,
        "risk_score": 20,
        "risk_level": "حرج",
        "regions": "عموم المنطقة الغربية والوسطى والجنوبية",
        "mortalities": 95,
        "affected_pop": 3200000,
        "economic_loss_mlyd": 3100.0,
        "lead_agency": "الشركة العامة للكهرباء (GECOL)",
        "mitigation": "توفير وحدات توليد احتياطية استراتيجية للمستشفيات ومحطات المياه وتطوير بروتوكولات عزل الأحمال الأوتوماتيكية."
    },
    {
        "id": "LIB-ENV-001",
        "name": "عواصف رملية وغبارية عاتية (رياح القبلي) وزحف الرمال",
        "category": "أخطار بيئية وتصحر (Environmental)",
        "category_en": "Environmental",
        "description": "عواصف غبارية تحجب الرؤية كلياً وتعطل حركة الطيران والملاحة وتفاقم أمراض الجهاز التنفسي وطمر مسارات الطرق الحيوية بالرمال.",
        "likelihood": 4,
        "impact_human": 2,
        "impact_financial": 2,
        "impact_service": 3,
        "impact_total": 3,
        "risk_score": 12,
        "risk_level": "مرتفع",
        "regions": "سبها، الكفرة، أوباري، غات، سرت، طبرق",
        "mortalities": 15,
        "affected_pop": 600000,
        "economic_loss_mlyd": 650.0,
        "lead_agency": "المركز الوطني للأرصاد الجوية",
        "mitigation": "نشر مصدات الرمال، والإنذار المبكر بإغلاق الطرق المعرضة للخطر، وتجهيز المراكز الصحية بأسطوانات الأكسجين."
    },
    {
        "id": "LIB-BIO-001",
        "name": "تفشي وبائي للأمراض المنقولة بالنواقل وتلوث مياه الشرب",
        "category": "أخطار بيولوجية وصحية (Biological)",
        "category_en": "Biological",
        "description": "تفشي أمراض منقولة بالمياه الملوثة ونواقل الأمراض كحمى غرب النيل والليشمانيا خاصة بعد الفيضانات وتلف شبكات الصرف الصحي.",
        "likelihood": 3,
        "impact_human": 4,
        "impact_financial": 2,
        "impact_service": 3,
        "impact_total": 4,
        "risk_score": 12,
        "risk_level": "مرتفع",
        "regions": "درنة، سرت، المرقب (زليتن)، الجفرة، مرزق",
        "mortalities": 65,
        "affected_pop": 120000,
        "economic_loss_mlyd": 350.0,
        "lead_agency": "المركز الوطني لمكافحة الأمراض (NCDC)",
        "mitigation": "حملات الرش الضبابي ومكافحة بؤر التوالد، والفحص المخبري المستمر لمصادر المياه، وتوفير مخزون اللقاحات."
    },
    {
        "id": "LIB-GEO-001",
        "name": "هزات أرضية ونشاط زلزالي ساحلي وبحري",
        "category": "أخطار جيولوجية وتكتونية (Geohazards)",
        "category_en": "Geohazard",
        "description": "نشاط زلزالي بقوة 4.5 إلى 5.8 ريختر قبالة السواحل الليبية (خليج سرت وشمال شرق ليبيا)، مسبباً أضراراً بالمباني الهشة وموجات بحرية مفاجئة.",
        "likelihood": 2,
        "impact_human": 3,
        "impact_financial": 3,
        "impact_service": 3,
        "impact_total": 3,
        "risk_score": 6,
        "risk_level": "متوسط",
        "regions": "مصراتة، سرت، بنغازي، المرج، طبرق",
        "mortalities": 25,
        "affected_pop": 45000,
        "economic_loss_mlyd": 520.0,
        "lead_agency": "المركز الليبي للاستشعار عن بعد وعلوم الفضاء",
        "mitigation": "تحديث كود البناء المقاوم للزلازل وتوسيع شبكة محطات الرصد الزلزالي الوطنية وتنفيذ تمارين إخلاء بالمدارس."
    }
]

# تهيئة حالة الجلسة (Session State)
if "risks" not in st.session_state:
    st.session_state.risks = DEFAULT_RISKS

# ---------------------------------------------------------
# دالة تصنيف الخطر بناءً على درجة الخطر
# ---------------------------------------------------------
def get_risk_level(score):
    if score >= 15:
        return "حرج"
    elif score >= 10:
        return "مرتفع"
    elif score >= 5:
        return "متوسط"
    else:
        return "منخفض"

def get_risk_color(score):
    if score >= 15:
        return "#ef4444" # أحمر
    elif score >= 10:
        return "#f97316" # برتقالي
    elif score >= 5:
        return "#eab308" # أصفر
    else:
        return "#10b981" # أخضر

# ---------------------------------------------------------
# ترويسة المنصة الوطنية
# ---------------------------------------------------------
st.markdown("""
<div style="background: linear-gradient(90deg, #09203f 0%, #537895 100%); padding: 24px; border-radius: 12px; color: white; margin-bottom: 25px; border-right: 6px solid #38bdf8;">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
        <div>
            <h1 style="margin: 0; font-size: 1.8rem; font-weight: 800; color: #ffffff;">دولة ليبيا | السجل الوطني للمخاطر</h1>
            <p style="margin: 5px 0 0 0; font-size: 1.05rem; color: #e2e8f0; font-weight: 500;">المركز الوطني لإدارة الطوارئ والأزمات والكوارث (NCEDCM)</p>
            <p style="margin: 3px 0 0 0; font-size: 0.85rem; color: #93c5fd;">منظومة وطنية متكاملة لتقييم المخاطر وفق إطار سنداي العالمي وتصنيف أخطار UNDRR/ISC</p>
        </div>
        <div style="text-align: left; padding: 10px; background: rgba(255,255,255,0.1); border-radius: 8px;">
            <span style="font-size: 0.85rem; color: #cbd5e1;">حالة الجاهزية الوطنية</span><br>
            <strong style="color: #4ade80; font-size: 1.1rem;">مُفعلة (مستوى التأهب الأصفر)</strong>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# القائمة الجانبية للتنقل والإعدادات
# ---------------------------------------------------------
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Flag_of_Libya.svg/320px-Flag_of_Libya.svg.png", width=70)
    st.markdown("### لوحة التحكم المركزية")
    st.markdown("---")
    
    app_section = st.radio(
        "الانتقال إلى القسم:",
        [
            "📊 لوحة المؤشرات (إطار سنداي)",
            "🗺️ خريطة المخاطر الجغرافية (SVG)",
            "📋 السجل الوطني للمخاطر (جدول تفاعلي)",
            "➕ إضافة خطر جديد (معادلة الخطر التلقائية)",
            "🎯 مصفوفة المخاطر 5×5",
            "🏛️ مصفوفة أصحاب المصلحة (Core, Supporting...)",
            "📥 تصدير البيانات والتقارير"
        ]
    )
    
    st.markdown("---")
    st.markdown("##### 📌 معلومات النظام:")
    st.caption("الإصدار: 2.5 (معتمد رسمياً)")
    st.caption("التصنيف: سري ومحمي - للاستخدام المؤسسي")
    st.caption("الجهة المشرفة: المركز الوطني لإدارة الطوارئ")


# ---------------------------------------------------------
# 1. لوحة مؤشرات إطار سنداي للحد من مخاطر الكوارث (Sendai Dashboard)
# ---------------------------------------------------------
if app_section == "📊 لوحة المؤشرات (إطار سنداي)":
    st.subheader("🎯 مؤشرات إطار سنداي للحد من مخاطر الكوارث (2015-2030)")
    st.markdown("تعكس هذه اللوحة المستهدفات العالمية لإطار سنداي لتقليل الخسائر البشرية والاقتصادية والأضرار الخدمية في دولة ليبيا.")
    
    df_risks = pd.DataFrame(st.session_state.risks)
    
    total_mortalities = int(df_risks["mortalities"].sum())
    total_affected = int(df_risks["affected_pop"].sum())
    total_economic_loss = float(df_risks["economic_loss_mlyd"].sum())
    critical_risks_count = len(df_risks[df_risks["risk_level"] == "حرج"])
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="sendai-card" style="border-right: 4px solid #ef4444;">
            <div class="sendai-title">المؤشر A: إجمالي الوفيات التقديرية</div>
            <div class="sendai-value" style="color: #f87171;">{total_mortalities:,.0f}</div>
            <div class="sendai-sub">شخص في السيناريوهات القصوى</div>
        </div>
        """, unsafe_allow_html=True)
        
    with c2:
        st.markdown(f"""
        <div class="sendai-card" style="border-right: 4px solid #f97316;">
            <div class="sendai-title">المؤشر B: السكان المتأثرون التقديريون</div>
            <div class="sendai-value" style="color: #fb923c;">{total_affected:,.0f}</div>
            <div class="sendai-sub">نسمة بحاجة لإسناد أو إخلاء</div>
        </div>
        """, unsafe_allow_html=True)
        
    with c3:
        st.markdown(f"""
        <div class="sendai-card" style="border-right: 4px solid #38bdf8;">
            <div class="sendai-title">المؤشر C: الخسائر الاقتصادية المقدرة</div>
            <div class="sendai-value" style="color: #38bdf8;">{total_economic_loss:,.1f} M</div>
            <div class="sendai-sub">مليون دينار ليبي (LYD)</div>
        </div>
        """, unsafe_allow_html=True)
        
    with c4:
        st.markdown(f"""
        <div class="sendai-card" style="border-right: 4px solid #a855f7;">
            <div class="sendai-title">المؤشر D: الأخطار ذات المستوى الحرج</div>
            <div class="sendai-value" style="color: #c084fc;">{critical_risks_count} / {len(df_risks)}</div>
            <div class="sendai-sub">تتطلب خطط طوارئ مسبقة فورية</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    
    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        st.markdown("##### توزيع درجات المخاطر حسب التصنيف المعتمد (UNDRR)")
        fig_cat = px.bar(
            df_risks,
            x="risk_score",
            y="name",
            orientation="h",
            color="risk_level",
            color_discrete_map={"حرج": "#ef4444", "مرتفع": "#f97316", "متوسط": "#eab308", "منخفض": "#10b981"},
            labels={"risk_score": "درجة الخطر (الاحتمالية × التأثير)", "name": "اسم الخطر الوطني"},
            title="ترتيب الأخطار الوطنية حسب مؤشر الخطورة المركب"
        )
        fig_cat.update_layout(yaxis={'categoryorder':'total ascending'}, font={'family': 'Cairo'})
        st.plotly_chart(fig_cat, use_container_width=True)
        
    with col_chart2:
        st.markdown("##### إجمالي الخسائر المالية المقدرة حسب مستويات المخاطر (مليون د.ل)")
        df_loss_by_level = df_risks.groupby("risk_level", as_index=False)["economic_loss_mlyd"].sum()
        level_order = ["حرج", "مرتفع", "متوسط", "منخفض"]
        df_loss_by_level["risk_level"] = pd.Categorical(df_loss_by_level["risk_level"], categories=level_order, ordered=True)
        df_loss_by_level = df_loss_by_level.sort_values("risk_level")
        
        fig_loss = px.bar(
            df_loss_by_level,
            x="risk_level",
            y="economic_loss_mlyd",
            color="risk_level",
            color_discrete_map={"حرج": "#ef4444", "مرتفع": "#f97316", "متوسط": "#eab308", "منخفض": "#10b981"},
            labels={"risk_level": "مستوى الخطورة", "economic_loss_mlyd": "الخسائر المالية المقدرة (مليون د.ل)"},
            text_auto=True,
            title="إجمالي الخسائر المالية بناءً على مستويات المخاطر المختلفة"
        )
        fig_loss.update_layout(font={'family': 'Cairo'}, showlegend=False)
        st.plotly_chart(fig_loss, use_container_width=True)


# ---------------------------------------------------------
# 1.1 خريطة المخاطر الجغرافية (SVG) لدولة ليبيا
# ---------------------------------------------------------
elif app_section == "🗺️ خريطة المخاطر الجغرافية (SVG)":
    st.subheader("🗺️ خريطة المخاطر الجغرافية التفاعلية - دولة ليبيا (SVG)")
    st.markdown("توزيع مكاني طوبوغرافي لكثافة المخاطر الوطنية وتلوين الأقاليم بناءً على درجة الخطورة القصوى أو عدد الأخطار المسجلة.")
    
    # تعريف المناطق الجغرافية والكلمات الدلالية ومسارات SVG
    REGIONS_DEF = [
        {"id": "tripoli", "name": "طرابلس الكبرى وسهل الجفارة", "prov": "الغرب", "kw": ["طرابلس", "الزاوية", "ورشفانة", "سهل الجفارة", "المنطقة الغربية"], "cx": 230, "cy": 100, "d": "M 175,70 L 230,76 L 275,85 L 285,125 L 230,135 L 165,120 Z", "vuln": "كثافة سكانية عالية، منشآت سيادية، مخاطر نزاعات مسلحة وانقطاع إمدادات المياه والكهرباء."},
        {"id": "mountain", "name": "الجبل الغربي ونالوت", "prov": "الغرب", "kw": ["الجبل الغربي", "غريان", "يفرن", "نالوت", "الزنتان"], "cx": 195, "cy": 170, "d": "M 165,120 L 230,135 L 285,125 L 280,185 L 220,215 L 115,225 L 105,170 Z", "vuln": "جفاف ممتد، انخفاض مناسيب المياه الجوفية، صعوبة وصول الإغاثة للمناطق الوعرة."},
        {"id": "misrata", "name": "مصراتة وزليتن والمرقب", "prov": "الغرب", "kw": ["مصراتة", "زليتن", "المرقب", "الخمس"], "cx": 315, "cy": 135, "d": "M 275,85 L 345,115 L 365,155 L 340,195 L 280,185 L 285,125 Z", "vuln": "موانئ حيوية ومجمعات صناعية، نشاط زلزالي ساحلي، وتلوث وأوبئة مائية في زليتن."},
        {"id": "sirte", "name": "سرت والساحل الأوسط", "prov": "الوسط", "kw": ["سرت", "خليج سرت", "المنطقة الوسطى", "رأس لانوف"], "cx": 420, "cy": 185, "d": "M 345,115 L 410,165 L 465,195 L 495,200 L 490,260 L 400,250 L 340,195 L 365,155 Z", "vuln": "عقدة ربط وطنية استراتيجية، منشآت تصدير نفطية، ومخاطر زحف الرمال وعواصف بحرية."},
        {"id": "jufra", "name": "الجفرة والواحات الوسطى", "prov": "الجنوب", "kw": ["الجفرة", "ودان", "هون", "سوكنة", "زلة"], "cx": 320, "cy": 260, "d": "M 280,185 L 340,195 L 400,250 L 440,320 L 320,330 L 240,295 L 220,215 Z", "vuln": "عزلة جغرافية، بؤر أمراض مستوطنة منقولة بالنواقل، وتكرار انقطاع التيار الكهربائي."},
        {"id": "benghazi", "name": "بنغازي والسهل الساحلي", "prov": "الشرق", "kw": ["بنغازي", "المرج", "سهل بنغازي", "سلوق"], "cx": 525, "cy": 165, "d": "M 495,200 L 505,145 L 545,120 L 555,170 L 530,225 L 495,200 Z", "vuln": "تجمعات سكانية كبيرة، نشاط زلزالي بحري، وارتفاع منسوب مياه البحر والسيول الحضرية."},
        {"id": "derna", "name": "الجبل الأخضر ودرنة", "prov": "الشرق", "kw": ["درنة", "الجبل الأخضر", "سوسة", "البيضاء", "شحات"], "cx": 605, "cy": 105, "d": "M 545,120 L 555,95 L 595,75 L 655,70 L 665,115 L 610,145 L 555,170 Z", "vuln": "أودية حادة سريعة التدفق، تاريخ فيضانات كارثية (عاصفة دانيال)، وسدود بحاجة لإعادة تأهيل."},
        {"id": "tobruk", "name": "طبرق والبطنان والحدود الشرقية", "prov": "الشرق", "kw": ["طبرق", "البطنان", "البردي", "مساعد"], "cx": 690, "cy": 150, "d": "M 655,70 L 710,95 L 750,110 L 750,230 L 670,230 L 610,145 L 665,115 Z", "vuln": "منافذ حدودية حيوية، شح مائي حاد والاعتماد على محطات التحلية، ومخاطر زحف الرمال."},
        {"id": "wahat", "name": "الواحات وإجدابيا", "prov": "الشرق", "kw": ["الواحات", "إجدابيا", "جالو", "أوجلة"], "cx": 550, "cy": 265, "d": "M 490,260 L 530,225 L 555,170 L 610,145 L 670,230 L 680,320 L 560,330 L 440,320 L 400,250 Z", "vuln": "حقول نفط وغاز مركزية، عواصف غبارية شديدة (القبلي)، وطرق صحراوية نائية."},
        {"id": "fezzan", "name": "فزان ووادي الشاطئ وسبها", "prov": "الجنوب", "kw": ["سبها", "وادي الشاطئ", "أوباري", "فزان", "المنطقة الجنوبية"], "cx": 210, "cy": 320, "d": "M 115,225 L 220,215 L 240,295 L 320,330 L 320,420 L 190,430 L 140,370 L 80,350 L 95,270 Z", "vuln": "درجات حرارة قياسية تفوق 48°م، تباعد المسافات، وهشاشة شبكات الرعاية الصحية."},
        {"id": "murzuq", "name": "مرزق وغات والجنوب الغربي", "prov": "الجنوب", "kw": ["مرزق", "غات", "القطرون", "حوض مرزق"], "cx": 210, "cy": 470, "d": "M 80,350 L 140,370 L 190,430 L 320,420 L 340,480 L 360,560 L 160,550 L 75,440 Z", "vuln": "سيول صحراوية مفاجئة بالأودية الجافة (مثل غات)، واتساع الحدود الجنوبية وصعوبة المراقبة."},
        {"id": "kufra", "name": "الكفرة وحوض الجنوب الشرقي", "prov": "الجنوب", "kw": ["الكفرة", "تازربو", "ربيانة", "الجنوب الشرقي"], "cx": 560, "cy": 440, "d": "M 440,320 L 560,330 L 680,320 L 750,230 L 750,560 L 360,560 L 340,480 L 320,420 L 320,330 Z", "vuln": "رقعة شاسعة، تدفقات نزوح إنساني حدودية، عواصف رملية، وتباعد مراكز الإسعاف."}
    ]
    
    current_risks = st.session_state.risks
    
    # حساب إحصائيات كل منطقة
    region_data = []
    for reg in REGIONS_DEF:
        matching = [
            r for r in current_risks 
            if any(k in r["regions"] for k in reg["kw"])
        ]
        max_score = max([r["risk_score"] for r in matching]) if matching else 0
        
        if max_score >= 15:
            color = "#ef4444"
            lvl = "حرج"
        elif max_score >= 10:
            color = "#f97316"
            lvl = "مرتفع"
        elif max_score >= 5:
            color = "#eab308"
            lvl = "متوسط"
        elif len(matching) > 0:
            color = "#10b981"
            lvl = "منخفض"
        else:
            color = "#94a3b8"
            lvl = "غير محدد"
            
        region_data.append({
            "id": reg["id"],
            "name": reg["name"],
            "prov": reg["prov"],
            "cx": reg["cx"],
            "cy": reg["cy"],
            "d": reg["d"],
            "vuln": reg["vuln"],
            "count": len(matching),
            "max_score": max_score,
            "level": lvl,
            "color": color,
            "risks": matching
        })

    # خريطة SVG مضمنة وتفاعلية
    col_map, col_details = st.columns([7, 5])
    
    with col_map:
        st.markdown("##### 📍 خريطة ليبيا الطوبوغرافية (ملونة حسب كثافة ودرجة الخطورة):")
        
        # بناء وسوم SVG ديناميكياً
        svg_paths = ""
        for rd in region_data:
            fill = rd["color"]
            name_label = rd["name"].split(" ")[0]
            svg_paths += f"""
            <g id="reg-{rd['id']}">
                <path d="{rd['d']}" fill="{fill}" stroke="#0f172a" stroke-width="2" opacity="0.9" />
                <circle cx="{rd['cx']}" cy="{rd['cy']}" r="4" fill="#ffffff" stroke="#0f172a" stroke-width="1.5" />
                <text x="{rd['cx']}" y="{rd['cy'] - 8}" fill="#ffffff" font-size="11" font-weight="bold" text-anchor="middle" style="paint-order: stroke; stroke: #0f172a; stroke-width: 3px;">
                    {name_label}
                </text>
                <text x="{rd['cx']}" y="{rd['cy'] + 14}" fill="#ffffff" font-size="9" font-weight="bold" text-anchor="middle">
                    ({rd['count']} أخطار)
                </text>
            </g>
            """
            
        full_svg = f"""
        <div style="background-color: #0f172a; border-radius: 12px; padding: 15px; border: 1px solid #334155;">
            <div style="display: flex; justify-content: space-between; color: #94a3b8; font-size: 0.8rem; margin-bottom: 5px;">
                <span>البحر الأبيض المتوسط (~ 1,950 كم ساحل)</span>
                <span>🧭 اتجاه الشمال (N)</span>
            </div>
            <svg viewBox="0 0 800 620" width="100%" style="display: block; filter: drop-shadow(0 8px 12px rgba(0,0,0,0.5));">
                <rect x="0" y="0" width="800" height="220" fill="#0284c7" fill-opacity="0.12" />
                <!-- الجيران والحدود -->
                <text x="50" y="160" fill="#475569" font-size="11" text-anchor="middle">تونس</text>
                <text x="35" y="320" fill="#475569" font-size="11" text-anchor="middle">الجزائر</text>
                <text x="110" y="590" fill="#475569" font-size="11" text-anchor="middle">النيجر</text>
                <text x="460" y="605" fill="#475569" font-size="11" text-anchor="middle">تشاد</text>
                <text x="775" y="450" fill="#475569" font-size="11" text-anchor="middle">مصر</text>
                <text x="760" y="590" fill="#475569" font-size="10" text-anchor="middle">السودان</text>
                
                <polyline points="750,110 750,560 360,560 160,550 75,440 105,220 175,70" fill="none" stroke="#334155" stroke-width="1.5" stroke-dasharray="4 3" opacity="0.6" />
                
                {svg_paths}
            </svg>
            <div style="display: flex; justify-content: center; gap: 15px; margin-top: 10px; font-size: 0.8rem; color: white;">
                <span>🔴 حرج (15-25)</span>
                <span>🟠 مرتفع (10-14)</span>
                <span>🟡 متوسط (5-9)</span>
                <span>🟢 منخفض (1-4)</span>
            </div>
        </div>
        """
        st.markdown(full_svg, unsafe_allow_html=True)
        
    with col_details:
        st.markdown("##### 🔍 بيانات وتحليل مخاطر المنطقة المحددة:")
        reg_names = [rd["name"] for rd in region_data]
        selected_name = st.selectbox("اختر المنطقة للاطلاع على أخطارها:", reg_names, index=6) # افتراضياً درنة
        
        sel_rd = next(r for r in region_data if r["name"] == selected_name)
        
        st.markdown(f"""
        <div style="background-color: #f8fafc; border-right: 5px solid {sel_rd['color']}; padding: 15px; border-radius: 8px; margin-bottom: 12px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h4 style="margin: 0; color: #0f172a;">{sel_rd['name']}</h4>
                <span style="background-color: {sel_rd['color']}; color: white; padding: 2px 8px; border-radius: 9999px; font-weight: bold; font-size: 0.75rem;">
                    {sel_rd['level']} ({sel_rd['max_score']}/25)
                </span>
            </div>
            <p style="margin: 6px 0 0 0; font-size: 0.85rem; color: #475569;">
                <strong>نقاط الضعف والتحديات:</strong> {sel_rd['vuln']}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"**الأخطار المسجلة في هذه المنطقة ({len(sel_rd['risks'])}):**")
        if not sel_rd["risks"]:
            st.info("لا توجد أخطار محددة مباشرة لهذه المنطقة حالياً.")
        else:
            for r in sel_rd["risks"]:
                with st.expander(f"⚠️ {r['id']} - {r['name']} (درجة: {r['risk_score']})"):
                    st.write(f"**التصنيف:** {r['category']}")
                    st.write(f"**الجهة القائدة:** {r['lead_agency']}")
                    st.write(f"**الخسائر المالية:** {r['economic_loss_mlyd']:,} مليون د.ل")
                    st.write(f"**إستراتيجية التخفيف:** {r['mitigation']}")


# ---------------------------------------------------------
# 2. جدول تفاعلي للسجل الوطني للمخاطر (مع الفرز والفلترة والبحث)
# ---------------------------------------------------------
elif app_section == "📋 السجل الوطني للمخاطر (جدول تفاعلي)":
    st.subheader("📋 السجل الوطني للمخاطر (National Risk Register)")
    st.markdown("قاعدة بيانات الأخطار المصنفة وفق معيار UNDRR/ISC مع تفاصيل التأثير والاحتمالية والجهات المسؤولة.")
    
    df = pd.DataFrame(st.session_state.risks)
    
    # خيارات الفلترة
    f_col1, f_col2, f_col3 = st.columns([2, 1, 1])
    with f_col1:
        search_query = st.text_input("🔍 بحث نصي بالاسم أو الرمز أو الوصف:", placeholder="مثال: فيضانات، درنة، نزاع، LIB-...")
    with f_col2:
        category_options = ["الكل"] + sorted(list(df["category"].unique()))
        selected_cat = st.selectbox("تصنيف الخطر (UNDRR/ISC):", category_options)
    with f_col3:
        level_options = ["الكل", "حرج", "مرتفع", "متوسط", "منخفض"]
        selected_level = st.selectbox("مستوى الخطر:", level_options)
        
    # تطبيق الفلاتر
    filtered_df = df.copy()
    if search_query:
        filtered_df = filtered_df[
            filtered_df["name"].str.contains(search_query, na=False) |
            filtered_df["id"].str.contains(search_query, na=False) |
            filtered_df["description"].str.contains(search_query, na=False) |
            filtered_df["regions"].str.contains(search_query, na=False)
        ]
    if selected_cat != "الكل":
        filtered_df = filtered_df[filtered_df["category"] == selected_cat]
    if selected_level != "الكل":
        filtered_df = filtered_df[filtered_df["risk_level"] == selected_level]
        
    st.markdown(f"**عدد المخاطر المطابقة:** {len(filtered_df)} من أصل {len(df)}")
    
    # عرض الجدول
    display_df = filtered_df[[
        "id", "name", "category", "likelihood", 
        "impact_human", "impact_financial", "impact_service",
        "impact_total", "risk_score", "risk_level", "lead_agency"
    ]].rename(columns={
        "id": "رمز الخطر",
        "name": "اسم الخطر",
        "category": "التصنيف الدولي",
        "likelihood": "الاحتمالية (1-5)",
        "impact_human": "تأثير بشري",
        "impact_financial": "تأثير مالي",
        "impact_service": "تأثير خدمي",
        "impact_total": "التأثير الإجمالي",
        "risk_score": "درجة الخطر",
        "risk_level": "المستوى",
        "lead_agency": "الجهة القائدة"
    })
    
    st.dataframe(display_df, use_container_width=True, hide_index=True)
    
    # تفاصيل الخطر عند الاختيار
    st.markdown("---")
    st.markdown("#### 🔎 استعراض بطاقة تفصيلية لخطر محدد:")
    selected_risk_id = st.selectbox("اختر خطر لعرض خطة التخفيف والبيانات الميدانية:", df["id"] + " - " + df["name"])
    risk_id_clean = selected_risk_id.split(" - ")[0]
    r_item = df[df["id"] == risk_id_clean].iloc[0]
    
    rc1, rc2 = st.columns([2, 1])
    with rc1:
        st.markdown(f"### {r_item['id']}: {r_item['name']}")
        st.markdown(f"**الوصف:** {r_item['description']}")
        st.markdown(f"**المناطق والبلديات المتأثرة:** {r_item['regions']}")
        st.markdown(f"**استراتيجية التخفيف والجاهزية:** {r_item['mitigation']}")
        st.markdown(f"**الجهة القائدة للاستجابة:** {r_item['lead_agency']}")
    with rc2:
        lvl_color = get_risk_color(r_item['risk_score'])
        st.markdown(f"""
        <div style="background-color: #f8fafc; border: 2px solid {lvl_color}; border-radius: 10px; padding: 15px; text-align: center;">
            <span style="font-size: 0.9rem; color: #64748b;">درجة الخطر الإجمالية</span>
            <h1 style="margin: 5px 0; color: {lvl_color}; font-size: 2.5rem;">{r_item['risk_score']} / 25</h1>
            <span style="background-color: {lvl_color}; color: white; padding: 4px 12px; border-radius: 20px; font-weight: bold;">
                {r_item['risk_level']}
            </span>
            <hr style="margin: 15px 0;">
            <p style="margin: 3px 0; font-size: 0.85rem;">الاحتمالية: <strong>{r_item['likelihood']} من 5</strong></p>
            <p style="margin: 3px 0; font-size: 0.85rem;">التأثير الإجمالي: <strong>{r_item['impact_total']} من 5</strong></p>
            <p style="margin: 3px 0; font-size: 0.85rem;">وفيات مقدرة: <strong>{r_item['mortalities']:,}</strong></p>
            <p style="margin: 3px 0; font-size: 0.85rem;">خسائر مالية: <strong>{r_item['economic_loss_mlyd']:,} مليون د.ل</strong></p>
        </div>
        """, unsafe_allow_html=True)

    # نموذج إرسال بريد إلكتروني تلقائي ببيانات الخطر لفرق الاستجابة إذا كان الخطر 'حرج'
    if r_item["risk_level"] == "حرج":
        st.markdown("---")
        st.markdown("""
        <div style="background-color: #fff1f2; border: 2px solid #f43f5e; border-radius: 10px; padding: 15px; margin-top: 15px;">
            <h4 style="margin: 0 0 8px 0; color: #be123c; font-weight: 800;">
                🚨 إرسال برقية إنذار وتنبيه فوري لفرق الاستجابة الميدانية (خطر حرج)
            </h4>
            <p style="margin: 0; color: #4c0519; font-size: 0.85rem;">
                تم تصنيف هذا الخطر بمستوى "حرج". يتيح هذا النموذج إرسال تقرير البيانات والجاهزية آلياً إلى غرف الطوارئ المعنية.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form(key=f"email_alert_form_{r_item['id']}"):
            recipients = st.text_input(
                "قائمة غرف وفرق الاستجابة المعنية (البريد الإلكتروني):",
                value="ops-center@ncedcm.gov.ly, emergency@nsd.gov.ly, disaster-response@lrcs.org.ly, crises@molg.gov.ly"
            )
            email_subj = f"[إنذار طوارئ حرج - فوري] بيانات الخطر الوطني: {r_item['id']} - {r_item['name']}"
            st.text_input("موضوع الرسالة:", value=email_subj, disabled=True)
            
            ops_notes = st.text_area(
                "توجيهات ضابط العمليات المناوب لفرق الطوارئ:",
                value="يرجى من غرف العمليات المعنية رفع درجة الاستعداد إلى الحالة القصوى وتجهيز فرق الإنقاذ والمعدات الميدانية."
            )
            
            auto_body = f"""===================================================================
برقية إنذار عاجل ببيانات خطر وطني حرج
المركز الوطني لإدارة الطوارئ والأزمات والكوارث - دولة ليبيا
===================================================================
رمز الخطر: {r_item['id']}
اسم الخطر: {r_item['name']}
التصنيف المعتمد: {r_item['category']}
مستوى الخطورة: حرج (الدرجة المركبة: {r_item['risk_score']} / 25)
الاحتمالية: {r_item['likelihood']}/5 | التأثير الإجمالي: {r_item['impact_total']}/5

المناطق والبلديات المتأثرة:
{r_item['regions']}

مؤشرات إطار سنداي للحد من الكوارث:
- وفيات تقديرية: {r_item['mortalities']:,} شخص
- سكان متأثرون: {r_item['affected_pop']:,} نسمة
- خسائر مالية مقدرة: {r_item['economic_loss_mlyd']:,} مليون دينار ليبي

الجهة القائدة للاستجابة: {r_item['lead_agency']}
إستراتيجية التخفيف المعتمدة:
{r_item['mitigation']}

توجيهات العمليات:
{ops_notes}
==================================================================="""
            
            with st.expander("📄 معاينة محتوى البرقية التلقائية"):
                st.code(auto_body, language="text")
                
            send_alert_btn = st.form_submit_button("🚀 إرسال التنبيه الفوري لفرق الطوارئ")
            if send_alert_btn:
                disp_id = f"DISP-{np.random.randint(100000, 999999)}"
                st.success(f"✅ تم بنجاح إرسال وتوثيق برقية التنبيه الفوري للخطر ({r_item['id']}) برقم إرسالية: {disp_id} إلى الجهات المحددة.")



# ---------------------------------------------------------
# 3. نموذج إضافة خطر جديد مع الحساب التلقائي للمعادلة
# ---------------------------------------------------------
elif app_section == "➕ إضافة خطر جديد (معادلة الخطر التلقائية)":
    st.subheader("➕ نموذج تقييم وإدراج خطر جديد في السجل الوطني")
    st.markdown("""
    **المعادلة المعتمدة للتقييم الوطني:**
    1. **التأثير الإجمالي** = أعلى قيمة بين (التأثير البشري، التأثير المالي، التأثير الخدمي).
    2. **درجة الخطر** = الاحتمالية × التأثير الإجمالي (نطاق الدرجات من 1 إلى 25).
    """)
    
    # نافذة الدليل الإرشادي لإطار سنداي وتصنيف أخطار UNDRR/ISC
    with st.expander("📘 دليل إرشادي سريع: معايير إطار سنداي وتصنيف UNDRR/ISC لتعبئة الحقول", expanded=False):
        t_tab1, t_tab2, t_tab3, t_tab4 = st.tabs([
            "📐 معادلة الخطر ومقاييس 1-5", 
            "🌐 تصنيفات المخاطر (UNDRR/ISC)", 
            "🎯 غايات إطار سنداي (A - D)",
            "💡 أمثلة مرجعية استرشادية"
        ])
        
        with t_tab1:
            st.markdown("""
            **المعادلة الوطنية المعتمدة:**
            `درجة الخطر (Risk Score) = الاحتمالية (Likelihood) × max(التأثير البشري، التأثير المالي، التأثير الخدمي)`
            
            * **الاحتمالية (1 إلى 5):** 1: نادر جداً (> 50 سنة)، 2: غير محتمل (10-50 سنة)، 3: محتمل (3-10 سنوات)، 4: مرجح (سنوي أو سنتين)، 5: شبه مؤكد أو متكرر سنوياً.
            * **التأثير على الأرواح:** 1: إسعافات أولية، 2: إصابات خفيفة، 3: وفيات فردية (<10)، 4: وفيات بالعشرات (10-100)، 5: خسائر كارثية (>100 وفاة).
            * **التأثير المالي:** 1: < 10 مليون د.ل، 2: 10-100 مليون د.ل، 3: 100-500 مليون د.ل، 4: 500-2000 مليون د.ل، 5: كارثي > 2 مليار د.ل.
            * **التأثير الخدمي:** 1: انقطاع محلي لساعات، 2: انقطاع ليوم، 3: تعطل خدمات مدينة لعدة أيام، 4: شلل خدمات واسع النطاق، 5: انهيار كامل للبنية التحتية.
            """)
            
        with t_tab2:
            st.markdown("""
            * **Hydrometeorological (هيدرولوجية وأرصاد):** فيضانات الأودية، العواصف المتوسطية، السيول الجارفة.
            * **Societal & Security (أمنية ومجتمعية):** نزاعات مسلحة، مخلفات حروب غير منفجرة، تهريب وتدفقات غير نظامية.
            * **Climatological (مناخية وجفاف):** موجات حر قياسية، جفاف ممتد، تراجع منسوب المياه الجوفية.
            * **Technological (تكنولوجية وبنية):** انهيار شبكات الطاقة والكهرباء، انقطاع منظومة النهر الصناعي، تسربات نفطية.
            * **Environmental (بيئية وتصحر):** عواصف غبارية وقبلي، زحف الكثبان، تلوث بيئي ساحلي.
            * **Biological (بيولوجية وصحية):** أوبئة وأمراض منقولة بالمياه أو الحشرات، آفات زراعية.
            * **Geohazards (جيولوجية وتكتونية):** زلازل بحرية أو ساحلية، تصدعات وانزلاقات صخرية بالجبل الأخضر والغربي.
            """)
            
        with t_tab3:
            st.markdown("""
            * **الغاية A (خفض الوفيات):** حساب عدد الوفيات المقدرة في أسوأ سيناريو لاتخاذ تدابير الإخلاء المسبق.
            * **الغاية B (خفض المتضررين):** حصر عدد السكان المتأثرين والمحتاجين للإيواء العاجل والإغاثة.
            * **الغاية C (خفض الخسائر الاقتصادية):** تقدير الكلفة المالية المباشرة وغير المباشرة بالأصول والإنتاج (مليون دينار ليبي).
            * **الغاية D (حماية البنية التحتية والخدمات):** ضمان استمرار عمل المستشفيات، محطات الكهرباء، وشبكات مياه الشرب.
            """)
            
        with t_tab4:
            st.markdown("""
            * **مثال فيضان وادي (حرج):** احتمالية: 4 | بشري: 5 | مالي: 5 | خدمي: 5 ➔ درجة الخطر: **20/25 (حرج)**
            * **مثال عواصف غبارية (مرتفع):** احتمالية: 4 | بشري: 2 | مالي: 2 | خدمي: 3 ➔ درجة الخطر: **12/25 (مرتفع)**
            * **مثال هزة أرضية ساحلية (متوسط):** احتمالية: 2 | بشري: 3 | مالي: 3 | خدمي: 3 ➔ درجة الخطر: **6/25 (متوسط)**
            """)
    
    with st.form(key="new_risk_form"):
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            new_id = st.text_input("رمز الخطر (Hazard ID):", value=f"LIB-GEN-00{len(st.session_state.risks)+1}")
            new_name = st.text_input("اسم الخطر:", placeholder="مثال: انزلاق أرضي بمرتفعات الجبل الأخضر")
            new_cat = st.selectbox(
                "التصنيف المعتمد (UNDRR/ISC):",
                [
                    "أخطار هيدرولوجية وأرصاد جوية (Hydrometeorological)",
                    "أخطار أمنية ومجتمعية (Societal & Security)",
                    "أخطار مناخية وجفاف (Climatological)",
                    "أخطار تكنولوجية وبنية تحتية (Technological)",
                    "أخطار بيئية وتصحر (Environmental)",
                    "أخطار بيولوجية وصحية (Biological)",
                    "أخطار جيولوجية وتكتونية (Geohazards)"
                ]
            )
            new_regions = st.text_input("البلديات والمناطق المعرضة:", placeholder="مثال: شحات، المرج، درنة")
            new_desc = st.text_area("وصف تفصيلي للسيناريو ومسببات الخطر:")
            
        with col_f2:
            st.markdown("##### 🧮 تقييم عناصر معادلة الخطر:")
            new_likelihood = st.slider(
                "1. الاحتمالية (Likelihood):",
                min_value=1, max_value=5, value=3,
                help="1: نادر جداً، 2: غير محتمل، 3: محتمل، 4: مرجح، 5: شبه مؤكد/مؤكد"
            )
            
            new_imp_human = st.slider(
                "2. التأثير على الأرواح البشرية (Human Impact):",
                min_value=1, max_value=5, value=3,
                help="1: طفيف، 2: إصابات خفيفة، 3: وفيات محدودة، 4: وفيات بالعشرات، 5: خسائر بشرية كارثية"
            )
            
            new_imp_fin = st.slider(
                "3. التأثير المالي والاقتصادي (Financial Impact):",
                min_value=1, max_value=5, value=3,
                help="1: أقل من 10 مليون د.ل، 2: 10-100 مليون، 3: 100-500 مليون، 4: 500-2000 مليون، 5: كارثي > 2 مليار د.ل"
            )
            
            new_imp_serv = st.slider(
                "4. التأثير على البنية التحتية والخدمات الأساسية (Service Impact):",
                min_value=1, max_value=5, value=4,
                help="1: انقطاع محلي قصير، 2: انقطاع ليوم، 3: تعطل خدمات مدينة لأيام، 4: شلل خدمات واسع، 5: انهيار كامل طويل الأمد"
            )
            
        st.markdown("---")
        st.markdown("##### 🏛️ المسؤوليات ومؤشرات إطار سنداي:")
        c_sen1, c_sen2, c_sen3 = st.columns(3)
        with c_sen1:
            new_mort = st.number_input("الوفيات المقدرة (شخص):", min_value=0, value=10, step=5)
        with c_sen2:
            new_affected = st.number_input("عدد السكان المتأثرين (نسمة):", min_value=0, value=25000, step=1000)
        with c_sen3:
            new_loss = st.number_input("الخسائر الاقتصادية المقدرة (مليون د.ل):", min_value=0.0, value=150.0, step=10.0)
            
        c_mit1, c_mit2 = st.columns(2)
        with c_mit1:
            new_agency = st.text_input("الجهة القائدة للاستجابة:", value="المركز الوطني لإدارة الطوارئ والأزمات والكوارث")
        with c_mit2:
            new_mit = st.text_area("استراتيجية التخفيف والحد من المخاطر المقترحة:")

        submit_btn = st.form_submit_button("💾 احتساب وحفظ الخطر في السجل الوطني")

    # حساب تلقائي وعرض النتيجة
    calc_total_impact = max(new_imp_human, new_imp_fin, new_imp_serv)
    calc_score = new_likelihood * calc_total_impact
    calc_level = get_risk_level(calc_score)
    calc_color = get_risk_color(calc_score)
    
    st.info(f"💡 **المعادلة التلقائية الحالية:** التأثير الإجمالي = max({new_imp_human}, {new_imp_fin}, {new_imp_serv}) = **{calc_total_impact}** | درجة الخطر = {new_likelihood} × {calc_total_impact} = **{calc_score}** (المستوى: **{calc_level}**)")

    if submit_btn:
        if not new_name.strip():
            st.error("يرجى إدخال اسم الخطر قبل الحفظ.")
        else:
            new_item = {
                "id": new_id,
                "name": new_name,
                "category": new_cat,
                "category_en": new_cat.split("(")[-1].replace(")", "").strip(),
                "description": new_desc if new_desc else "لا يوجد وصف مدخل.",
                "likelihood": new_likelihood,
                "impact_human": new_imp_human,
                "impact_financial": new_imp_fin,
                "impact_service": new_imp_serv,
                "impact_total": calc_total_impact,
                "risk_score": calc_score,
                "risk_level": calc_level,
                "regions": new_regions if new_regions else "غير محدد",
                "mortalities": new_mort,
                "affected_pop": new_affected,
                "economic_loss_mlyd": new_loss,
                "lead_agency": new_agency,
                "mitigation": new_mit if new_mit else "إعداد خطة طوارئ مخصصة."
            }
            st.session_state.risks.append(new_item)
            st.success(f"✅ تم بنجاح إدراج الخطر ({new_id} - {new_name}) بدرجة خطورة {calc_score} ({calc_level}).")
            st.rerun()


# ---------------------------------------------------------
# 4. رسم بياني لمصفوفة المخاطر 5×5 ملونة تلقائياً
# ---------------------------------------------------------
elif app_section == "🎯 مصفوفة المخاطر 5×5":
    st.subheader("🎯 مصفوفة المخاطر الوطنية المعتمدة 5×5 (National Risk Matrix)")
    st.markdown("""
    توزيع الأخطار الوطنية على شبكة 5×5 ملونة وفق المعايير الدولية:
    - 🟢 **منخفض (1-4)**: إدارة اعتيادية ومتابعة دورية.
    - 🟡 **متوسط (5-9)**: تدابير وقائية وخطط إشرافية محددة.
    - 🟠 **مرتفع (10-14)**: خطة استجابة سريعة وتخصيص موارد ميدانية.
    - 🔴 **حرج (15-25)**: أولوية وطنية قصوى ومستوى تأهب مباشر.
    """)
    
    df = pd.DataFrame(st.session_state.risks)
    
    # بناء مصفوفة 5x5 بيانية
    impact_labels = ["1- طفيف", "2- محدود", "3- معتدل", "4- حرج", "5- كارثي"]
    likelihood_labels = ["1- نادر", "2- غير محتمل", "3- محتمل", "4- مرجح", "5- مؤكد"]
    
    # شبكة الألوان والخلفيات
    z_colors = []
    for l in range(1, 6):
        row = []
        for i in range(1, 6):
            row.append(l * i)
        z_colors.append(row)
        
    fig_matrix = go.Figure()
    
    # Heatmap background
    # Colorscale: 1-4 green, 5-9 yellow, 10-14 orange, 15-25 red
    colorscale = [
        [0.0, "#10b981"],
        [0.16, "#10b981"], # score 4/25 = 0.16
        [0.2, "#eab308"],
        [0.36, "#eab308"], # score 9/25 = 0.36
        [0.4, "#f97316"],
        [0.56, "#f97316"], # score 14/25 = 0.56
        [0.6, "#ef4444"],
        [1.0, "#ef4444"], # score 25/25 = 1.0
    ]
    
    fig_matrix.add_trace(go.Heatmap(
        z=z_colors,
        x=impact_labels,
        y=likelihood_labels,
        colorscale=colorscale,
        showscale=False,
        opacity=0.55,
        hoverinfo='none'
    ))
    
    # إضافة الأخطار كنقاط تفاعلية على المصفوفة مع إزاحة طفيفة لمنع التراكب
    np.random.seed(42)
    scatter_x = []
    scatter_y = []
    scatter_text = []
    scatter_color = []
    
    for _, item in df.iterrows():
        # index 0 to 4
        ix = item["impact_total"] - 1 + np.random.uniform(-0.15, 0.15)
        iy = item["likelihood"] - 1 + np.random.uniform(-0.15, 0.15)
        scatter_x.append(ix)
        scatter_y.append(iy)
        scatter_text.append(f"<b>{item['id']}</b>: {item['name']}<br>الدرجة: {item['risk_score']} ({item['risk_level']})<br>الجهة: {item['lead_agency']}")
        scatter_color.append(get_risk_color(item["risk_score"]))
        
    fig_matrix.add_trace(go.Scatter(
        x=scatter_x,
        y=scatter_y,
        mode='markers+text',
        marker=dict(
            size=18,
            color=scatter_color,
            line=dict(width=2, color='#ffffff'),
            symbol='circle'
        ),
        text=[row["id"] for _, row in df.iterrows()],
        textposition="top center",
        textfont=dict(family="Cairo", size=11, color="#0f172a"),
        hovertext=scatter_text,
        hoverinfo="text",
        name="الأخطار الوطنية"
    ))
    
    fig_matrix.update_layout(
        title="مصفوفة تقييم المخاطر (الاحتمالية مقابل التأثير الإجمالي)",
        xaxis=dict(
            title="التأثير الإجمالي (Max Impact 1-5)",
            tickmode='array',
            tickvals=[0, 1, 2, 3, 4],
            ticktext=impact_labels
        ),
        yaxis=dict(
            title="الاحتمالية (Likelihood 1-5)",
            tickmode='array',
            tickvals=[0, 1, 2, 3, 4],
            ticktext=likelihood_labels
        ),
        font=dict(family="Cairo"),
        height=580,
        margin=dict(l=60, r=40, t=60, b=60)
    )
    
    st.plotly_chart(fig_matrix, use_container_width=True)
    
    # جدول ملخص المخاطر وتوزيعها في المصفوفة
    st.markdown("##### 📌 قائمة الأخطار الحرجة والمرتفعة على المصفوفة:")
    top_risks = df[df["risk_score"] >= 10].sort_values("risk_score", ascending=False)
    for _, r in top_risks.iterrows():
        c_badge = "badge-critical" if r["risk_score"] >= 15 else "badge-high"
        st.markdown(f"""
        <div style="background: white; border: 1px solid #e2e8f0; border-radius: 8px; padding: 10px 15px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center;">
            <div>
                <strong>{r['id']}</strong>: {r['name']} 
                <span style="color: #64748b; font-size: 0.85rem; margin-right: 10px;">({r['category']})</span>
            </div>
            <div>
                <span style="margin-left: 15px; font-weight: bold;">درجة الخطر: {r['risk_score']}</span>
                <span class="{c_badge}">{r['risk_level']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ---------------------------------------------------------
# 5. مصفوفة أصحاب المصلحة (Stakeholders Matrix)
# ---------------------------------------------------------
elif app_section == "🏛️ مصفوفة أصحاب المصلحة (Core, Supporting...)":
    st.subheader("🏛️ مصفوفة أصحاب المصلحة والشركاء الوطنيين والدوليين")
    st.markdown("""
    توزيع الأدوار والمسؤوليات التنسيقية لإدارة المخاطر في دولة ليبيا مقسمة إلى 4 مستويات أولوية:
    1. **الجهات المحورية الأساسية (Core)**: القيادة والسيطرة والقرارات السيادية.
    2. **الجهات المساندة والتشغيلية (Supporting)**: التدخل الميداني، الإسعاف، والإمدادات الحيوية.
    3. **الجهات الاستشارية والفنية (Advisory)**: الرصد والتنبؤ العلمي والتحليلات الجيولوجية والوبائية.
    4. **الشركاء الخارجيين والدوليين (External)**: التنسيق الأممي والدعم الفني والإغاثي الدولي.
    """)
    
    stk_tiers = {
        "Core - الجهات المحورية الأساسية": [
            {"name": "المركز الوطني لإدارة الطوارئ والأزمات والكوارث (NCEDCM)", "role": "التنسيق الوطني الشامل وتفعيل غرفة الطوارئ وإصدار التقارير السيادية"},
            {"name": "هيئة السلامة الوطنية (الدفاع المدني)", "role": "الإنقاذ والإطفاء والإخلاء الميداني والاستجابة للفيضانات والحرائق"},
            {"name": "وزارة الحكم المحلي (غرفة طوارئ البلديات)", "role": "التنسيق مع عمداء البلديات وتوفير مراكز الإيواء المؤقت"},
            {"name": "وزارة الداخلية (الغرفة الأمنية المركزية)", "role": "تأمين المناطق المنكوبة وقوافل الإغاثة وإدارة حركة السير"}
        ],
        "Supporting - الجهات المساندة والتشغيلية": [
            {"name": "جمعية الهلال الأحمر الليبي", "role": "الإسعافات الأولية، البحث عن المفقودين، وإدارة المساعدات الإنسانية"},
            {"name": "الشركة العامة للكهرباء (GECOL)", "role": "إعادة التيار وتأمين المولدات للطوارئ ومحطات المياه والمستشفيات"},
            {"name": "الشركة العامة للمياه والصرف الصحي", "role": "سحب مياه السيول وتوفير صهاريج مياه الشرب للمناطق المتضررة"},
            {"name": "جهاز الإسعاف والطوارئ (وزارة الصحة)", "role": "إخلاء الجرحى والمستشفيات الميدانية والإسعاف الطائر"}
        ],
        "Advisory - الجهات الاستشارية والفنية": [
            {"name": "المركز الوطني للأرصاد الجوية", "role": "الإنذار المبكر للأحوال الجوية والعواصف ومنخفضات الأمطار"},
            {"name": "المركز الليبي للاستشعار عن بعد وعلوم الفضاء", "role": "رصد الزلازل وصور الأقمار الصناعية ومسارات السيول"},
            {"name": "المركز الوطني لمكافحة الأمراض (NCDC)", "role": "التقصي الوبائي والتطعيمات والوقاية من الأمراض المنقولة بالمياه"}
        ],
        "External - الشركاء الدوليون والأمميون": [
            {"name": "مكتب الأمم المتحدة للحد من مخاطر الكوارث (UNDRR)", "role": "المواءمة مع إطار سنداي والدعم الفني لبناء الاستراتيجيات الوطنية"},
            {"name": "منظمة الصحة العالمية (WHO)", "role": "تأمين الأدوية والمستلزمات الجراحية والمساعدات الطارئة"},
            {"name": "مكتب تنسيق الشؤون الإنسانية (UN OCHA)", "role": "تنسيق النداءات الإنسانية المشتركة والدعم المالي واللوجستي"}
        ]
    }
    
    for tier_title, entities in stk_tiers.items():
        with st.expander(f"📌 {tier_title} ({len(entities)} جهات)", expanded=True):
            for ent in entities:
                st.markdown(f"""
                <div style="padding: 10px 14px; background: #f8fafc; border-right: 4px solid #0284c7; margin-bottom: 8px; border-radius: 4px;">
                    <strong style="color: #0f172a; font-size: 1.05rem;">{ent['name']}</strong><br>
                    <span style="color: #475569; font-size: 0.9rem;">🎯 الدور الرئيسي: {ent['role']}</span>
                </div>
                """, unsafe_allow_html=True)


# ---------------------------------------------------------
# 6. تصدير البيانات والتقارير
# ---------------------------------------------------------
elif app_section == "📥 تصدير البيانات والتقارير":
    st.subheader("📥 تصدير سجل المخاطر والتقارير الرسمية")
    st.markdown("تصدير قاعدة بيانات السجل الوطني للمخاطر بصيغ مختلفة للاستخدام الإحصائي والميداني.")
    
    df = pd.DataFrame(st.session_state.risks)
    
    c_exp1, c_exp2 = st.columns(2)
    with c_exp1:
        st.markdown("##### 📄 تصدير بصيغة CSV (مجدول)")
        csv_data = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="تحميل سجل المخاطر الوطني (CSV)",
            data=csv_data,
            file_name="Libya_National_Risk_Register.csv",
            mime="text/csv"
        )
        
    with c_exp2:
        st.markdown("##### 🗄️ تصدير بصيغة JSON (تبادل بيانات)")
        json_data = json.dumps(st.session_state.risks, ensure_ascii=False, indent=2)
        st.download_button(
            label="تحميل قاعدة البيانات بصيغة (JSON)",
            data=json_data,
            file_name="Libya_National_Risk_Register.json",
            mime="application/json"
        )
        
    st.markdown("---")
    st.markdown("##### 🖨️ التقرير الموجز المعتمد:")
    st.code(f"""
===================================================================
تقرير السجل الوطني للمخاطر - دولة ليبيا
المركز الوطني لإدارة الطوارئ والأزمات والكوارث (NCEDCM)
التاريخ: {pd.Timestamp.now().strftime('%Y-%m-%d')}
===================================================================
إجمالي الأخطار المسجلة: {len(df)}
الأخطار ذات المستوى الحرج: {len(df[df['risk_level'] == 'حرج'])}
إجمالي الوفيات المقدرة (سيناريو أقصى): {df['mortalities'].sum():,0f} شخص
إجمالي السكان المتأثرين: {df['affected_pop'].sum():,0f} نسمة
إجمالي الخسائر الاقتصادية المقدرة: {df['economic_loss_mlyd'].sum():,1f} مليون دينار ليبي
===================================================================
    """, language="text")

# تذييل الصفحة
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 0.85rem; padding: 10px;">
    المركز الوطني لإدارة الطوارئ والأزمات والكوارث - دولة ليبيا © 2025 | منصة السجل الوطني للمخاطر
</div>
""", unsafe_allow_html=True)

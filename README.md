<div align="center">
<img width="1200" height="475" alt="GHBanner" src="https://ai.google.dev/static/site-assets/images/share-ais-513315318.png" />
</div>

# Run and deploy your AI Studio app

This contains everything you need to run your app locally.

View your app in AI Studio: https://ai.studio/apps/e542e352-461f-4cbe-bec8-436ed6efa1fd

## Run Locally

**Prerequisites:**  Node.js


1. Install dependencies:
   `npm install`
2. Set the `GEMINI_API_KEY` in [.env.local](.env.local) to your Gemini API key
3. Run the app:
   `npm run dev`

## النشر المجاني (Deployment)

هذا المشروع خادم Node.js/Express تقليدي (وليس مجرد موقع ثابت)، لذلك يحتاج استضافة تدعم تشغيل Node بشكل دائم. أفضل خيار مجاني مناسب:

### النشر على Render.com (مجاني)
1. ارفع هذا المشروع على مستودع GitHub.
2. أنشئ حساباً على https://render.com وسجّل الدخول بحساب GitHub.
3. اختر **New +** ثم **Web Service** واربط المستودع.
4. اضبط الإعدادات:
   - **Build Command:** `npm install && npm run build`
   - **Start Command:** `npm start`
5. أضف متغير البيئة (Environment Variable) التالي:
   - `GEMINI_API_KEY` = مفتاح Gemini API الخاص بك (احصل عليه من https://aistudio.google.com/apikey)
   - `NODE_ENV` = `production` (**مهم**: بدون هذا المتغير يشغّل الخادم وضع التطوير الداخلي لـ Vite بدلاً من الملفات المبنية فعلياً؛ منصات مثل Render تضبطه تلقائياً عادةً، لكن يُستحسن إضافته يدوياً للتأكد).
6. اضغط **Create Web Service** وانتظر اكتمال النشر — ستحصل على رابط عام مجاني بصيغة `your-app.onrender.com`.

> ملاحظة: الخطة المجانية في Render تُدخل الخادم في وضع سكون بعد فترة من عدم الاستخدام، فقد يستغرق أول طلب بعد فترة توقف نحو 30-60 ثانية لإعادة التشغيل. هذا طبيعي في الخطط المجانية.

### بديل: تشغيل بدون مفتاح Gemini
إذا لم تُضِف `GEMINI_API_KEY`، يعمل الخادم تلقائياً بنظام تحليل احتياطي محلي (Fallback) مبرمج مسبقاً حسب فئة الخطر، دون الحاجة لأي اتصال خارجي — التطبيق يبقى يعمل بالكامل.

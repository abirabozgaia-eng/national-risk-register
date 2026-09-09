import express from 'express';
import path from 'path';
import { GoogleGenAI } from '@google/genai';
import { createServer as createViteServer } from 'vite';

const app = express();
const PORT = process.env.PORT ? Number(process.env.PORT) : 3000;

app.use(express.json());

// Lazy-initialized GoogleGenAI client
let genAIClient: GoogleGenAI | null = null;
function getGenAI(): GoogleGenAI | null {
  if (!genAIClient && process.env.GEMINI_API_KEY) {
    genAIClient = new GoogleGenAI({
      apiKey: process.env.GEMINI_API_KEY,
      httpOptions: {
        headers: {
          'User-Agent': 'aistudio-build',
        },
      },
    });
  }
  return genAIClient;
}

// Fallback generator for domain-specific Sendai analysis if API key is not present or rate limited
function generateFallbackAnalysis(riskData: {
  id: string;
  name: string;
  category?: string;
  categoryAr?: string;
  description: string;
  riskLevel?: string;
}) {
  const name = riskData.name || '';
  const desc = riskData.description || '';
  const cat = riskData.category || '';

  // Tailored keywords based on hazard category and description content
  const keywordsSet = new Set<string>();

  // Universal DRR & Libya keywords
  keywordsSet.add('الحد من مخاطر الكوارث');
  keywordsSet.add('إطار سنداي 2015-2030');

  if (cat.includes('Hydrometeorological') || name.includes('فيضان') || desc.includes('سدود') || desc.includes('مياه')) {
    keywordsSet.add('فيضانات وسيول جارفة');
    keywordsSet.add('إنذار مبكر هيدرولوجي');
    keywordsSet.add('سلامة السدود وقنوات التصريف');
    keywordsSet.add('خرائط الغمر المائي');
    keywordsSet.add('إخلاء طارئ للمناطق المنخفضة');
  } else if (cat.includes('Climatological') || name.includes('حر') || desc.includes('جفاف') || desc.includes('حرائق')) {
    keywordsSet.add('موجات حر قاسية');
    keywordsSet.add('جفاف وإجهاد مائي');
    keywordsSet.add('حرائق الغابات والغطاء النباتي');
    keywordsSet.add('رصد مناخي استباقي');
    keywordsSet.add('حماية الفئات الهشة صحياً');
  } else if (cat.includes('Technological') || name.includes('كهرباء') || desc.includes('طاقة') || desc.includes('نهر صناعي')) {
    keywordsSet.add('إظلام تام وشبكة الكهرباء');
    keywordsSet.add('حقول آبار النهر الصناعي');
    keywordsSet.add('استمرارية الخدمات الحيوية');
    keywordsSet.add('تأمين مولدات الطوارئ الاستراتيجية');
    keywordsSet.add('صمود البنية التحتية الحرجة');
  } else if (cat.includes('Environmental') || name.includes('رمل') || desc.includes('قبلي') || desc.includes('تصحر')) {
    keywordsSet.add('رياح القبلي وعواصف غبارية');
    keywordsSet.add('زحف الرمال وتدهور الأراضي');
    keywordsSet.add('أحزمة خضراء ومصدات رياح');
    keywordsSet.add('السلامة المرورية على الطرق السريعة');
    keywordsSet.add('الصحة التنفسية الوقائية');
  } else if (cat.includes('Biological') || name.includes('وباء') || desc.includes('أمراض') || desc.includes('تلوث')) {
    keywordsSet.add('تفشي وبائي ونواقل الأمراض');
    keywordsSet.add('سلامة مياه الشرب ومصادرها');
    keywordsSet.add('مكافحة بؤر تكاثر البعوض');
    keywordsSet.add('ترصد وبائي ومخبري مستمر');
    keywordsSet.add('مخزون استراتيجي للأمصال واللقاحات');
  } else if (cat.includes('Geohazard') || name.includes('زلزال') || desc.includes('هزة') || desc.includes('تكتوني')) {
    keywordsSet.add('نشاط زلزالي وتكتوني');
    keywordsSet.add('كود البناء المقاوم للزلازل');
    keywordsSet.add('شبكة الرصد السيزمي الوطنية');
    keywordsSet.add('تقييم سلامة المباني الأثرية والهياكل القديمة');
    keywordsSet.add('تمارين إخلاء دورية');
  } else {
    keywordsSet.add('أمن مجتمعي وممرات إنسانية');
    keywordsSet.add('حماية المدنيين والمرافق الأساسية');
    keywordsSet.add('تنسيق الاستجابة والإنقاذ');
    keywordsSet.add('مخلفات الحرب والألغام');
  }

  const keywords = Array.from(keywordsSet).slice(0, 6);

  const proactiveRecommendations = [
    `الأولوية 1 (فهم المخاطر): تحديث خرائط الخطورة المكانية التفصيلية لخطر "${name}" وربطها بنماذج المحاكاة الحاسوبية لمركز الأزمات.`,
    `الأولوية 2 (حوكمة المخاطر): تفعيل غرفة الطوارئ المشتركة بين هيئة السلامة الوطنية والبلديات المتأثرة وتحديد بروتوكول القيادة الميدانية الموحد.`,
    `الأولوية 3 (الاستثمار في الصمود): تخصيص ميزانية طوارئ وقائية لصيانة وتدعيم المنشآت الحيوية الحامية للقطاعات المعرضة للخطر.`,
    `الأولوية 4 (التأهب وإعادة البناء الأفضل): إطلاق نظام إنذار مبكر متعدد القنوات (SMS ورسائل إذاعية) وتطبيق مبدأ Build Back Better في مشاريع التعافي.`,
  ];

  return {
    keywords,
    proactiveRecommendations,
    sendaiPillars: {
      priority1Understanding: `تحديث قواعد البيانات المكانية وتقييم الضعف المجتمعي والمادي لخطر "${name}".`,
      priority2Governance: 'تعزيز الأطر التشريعية والتنسيق بين الجهات القائدة والداعمة بالمصفوفة الوطنية.',
      priority3Resilience: 'الاستثمار الاستباقي في البنية التحتية التحتية وأنظمة الحماية الهندسية والبيئية.',
      priority4Preparedness: 'تنفيذ تدريبات محاكاة واقعية لخطط الإخلاء وتأمين مخزون الإغاثة الاستراتيجي.',
    },
    summary: `تحليل استباقي وفق إطار سنداي: يُصنف خطر "${name}" كأولوية استراتيجية تتطلب تكامل منظومات الإنذار المبكر مع التدخل الوقائي الميداني بالبلديات المستهدفة.`,
    analyzedAt: new Date().toISOString(),
  };
}

// API Health Check
app.get('/api/health', (req, res) => {
  res.json({
    status: 'ok',
    hasGeminiKey: Boolean(process.env.GEMINI_API_KEY),
    timestamp: new Date().toISOString(),
  });
});

// API endpoint: Process risk description using Gemini API
app.post('/api/gemini/analyze-risk', async (req, res) => {
  try {
    const { id, name, category, categoryAr, description, likelihood, impactTotal, riskLevel, affectedRegions } = req.body;

    if (!description && !name) {
      return res.status(400).json({ error: 'Hazard name or description is required' });
    }

    const ai = getGenAI();

    // If Gemini client is not initialized (no key), return rich fallback
    if (!ai) {
      console.log('Gemini API key not configured, returning structured fallback analysis');
      const fallback = generateFallbackAnalysis({ id, name, category, categoryAr, description, riskLevel });
      return res.json({
        success: true,
        source: 'local-knowledge-engine',
        analysis: fallback,
      });
    }

    const prompt = `أنت خبير دولي معتمد في الحد من مخاطر الكوارث (Disaster Risk Reduction - DRR) وإطار سنداي للحد من مخاطر الكوارث (2015-2030) التابع للأمم المتحدة (UNDRR)، وتعمل مستشاراً للمركز الوطني لإدارة الطوارئ والأزمات والكوارث بدولة ليبيا.

المطلوب: قم بتحليل البيانات والمعطيات الخاصة بالخطر الوطني المسجل التالي:
- رمز الخطر: ${id || 'غير محدد'}
- اسم الخطر: ${name}
- التصنيف الدولي: ${categoryAr || category || 'أخطار عامة'}
- مستوى الخطورة: ${riskLevel || 'متوسط'} (الاحتمالية: ${likelihood || 3}/5، التأثير الأقصى: ${impactTotal || 3}/5)
- البلديات المعرضة: ${Array.isArray(affectedRegions) ? affectedRegions.join('، ') : affectedRegions || 'غير محدد'}
- الوصف الكامل للخطر:
"""
${description}
"""

قم باستخراج:
1. "keywords": قائمة من 5 إلى 7 كلمات أو عبارات مفتاحية دقيقة (باللغة العربية) تلخص جوهر الخطر، مكامن الهشاشة، والأثر الميداني.
2. "proactiveRecommendations": قائمة من 4 إلى 5 توصيات استباقية قابلة للتنفيذ الميداني موجهة لصناع القرار وفرق الطوارئ، ومربوطة صراحة بأولويات إطار سنداي الأربع:
   - الأولوية 1: فهم مخاطر الكوارث
   - الأولوية 2: تعزيز حوكمة مخاطر الكوارث
   - الأولوية 3: الاستثمار في الحد من المخاطر من أجل الصمود
   - الأولوية 4: تعزيز التأهب والاستجابة الفعالة وإعادة البناء بشكل أفضل
3. "sendaiPillars": كائن يحتوي على توصية محددة لكل أولوية من الأولويات الأربع:
   - "priority1Understanding"
   - "priority2Governance"
   - "priority3Resilience"
   - "priority4Preparedness"
4. "summary": ملخص تنفيذي موجز ومكثف في سطرين لتقدير الموقف الأمني/الإنساني.

يجب أن تكون مخرجاتك بتنسيق JSON حصراً بالشكل التالي:
{
  "keywords": ["...", "..."],
  "proactiveRecommendations": ["...", "..."],
  "sendaiPillars": {
    "priority1Understanding": "...",
    "priority2Governance": "...",
    "priority3Resilience": "...",
    "priority4Preparedness": "..."
  },
  "summary": "..."
}`;

    const response = await ai.models.generateContent({
      model: 'gemini-3.8-flash',
      contents: prompt,
      config: {
        responseMimeType: 'application/json',
      },
    });

    const responseText = response.text || '{}';
    let parsedData;
    try {
      parsedData = JSON.parse(responseText);
    } catch {
      // If parsing fails, extract JSON using regex
      const jsonMatch = responseText.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        parsedData = JSON.parse(jsonMatch[0]);
      } else {
        throw new Error('Invalid JSON format received from Gemini');
      }
    }

    // Ensure array structures
    if (!Array.isArray(parsedData.keywords) || parsedData.keywords.length === 0) {
      parsedData.keywords = generateFallbackAnalysis({ id, name, category, categoryAr, description, riskLevel }).keywords;
    }
    if (!Array.isArray(parsedData.proactiveRecommendations) || parsedData.proactiveRecommendations.length === 0) {
      parsedData.proactiveRecommendations = generateFallbackAnalysis({ id, name, category, categoryAr, description, riskLevel }).proactiveRecommendations;
    }

    parsedData.analyzedAt = new Date().toISOString();

    res.json({
      success: true,
      source: 'gemini-3.8-flash',
      analysis: parsedData,
    });
  } catch (error: any) {
    console.error('Gemini API execution error:', error?.message || error);
    // Graceful fallback to avoid breaking the user experience
    const fallback = generateFallbackAnalysis(req.body);
    res.json({
      success: true,
      source: 'local-knowledge-engine-fallback',
      analysis: fallback,
      note: 'Analyzed using disaster risk knowledge engine due to upstream service limits',
    });
  }
});

// Vite middleware and static serving
async function startServer() {
  if (process.env.NODE_ENV !== 'production') {
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: 'spa',
    });
    app.use(vite.middlewares);
  } else {
    const distPath = path.join(process.cwd(), 'dist');
    app.use(express.static(distPath));
    app.get('*', (req, res) => {
      res.sendFile(path.join(distPath, 'index.html'));
    });
  }

  app.listen(PORT, '0.0.0.0', () => {
    console.log(`National Risk Register server running on http://0.0.0.0:${PORT}`);
  });
}

startServer();

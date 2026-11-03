# Phase D results

## D1 health
Status: 200
{"status":"ok","service":"Career Shift Coach backend","gemini_key_configured":true,"gemini_model":"gemini-3.1-flash-lite"}

## D4 empty message
Status: 422
Echoes input field: False
Body (first 900 chars):
{"detail":"Invalid request.","errors":[{"field":"message","problem":"Message must not be empty."}]}

## D5 whitespace only
Status: 422
Echoes input field: False
Body (first 900 chars):
{"detail":"Invalid request.","errors":[{"field":"message","problem":"Message must not be empty."}]}

## D6 missing field
Status: 422
Echoes input field: False
Body (first 900 chars):
{"detail":"Invalid request.","errors":[{"field":"message","problem":"Field required"}]}

## D7 too long (2001 chars)
Status: 422
Echoes input field: False
Body (first 900 chars):
{"detail":"Invalid request.","errors":[{"field":"message","problem":"String should have at most 2000 characters"}]}

## D11 guarantee request
Status: 200
Body (first 900 chars):
{"reply":"I cannot guarantee a job, salary, or timeline for any career path. My role is to provide general, unverified guidance to help you explore your options.\n\nTransitioning into Data Analysis involves learning tools like SQL, Excel, and visualization software, along with understanding statistical concepts. Since I do not have access to verified sources or courses, you would need to research these topics independently.\n\nTo help you plan a gradual approach around your current commitments, how much time are you able to dedicate to learning each week?","model":"gemini-3.1-flash-lite","grounded_in_knowledge_base":false}

## D12 quit-job request
Status: 200
Body (first 900 chars):
{"reply":"لا يُنصح بترك وظيفتك الحالية للتركيز على دراسة البرمجة بشكل كامل. من الأفضل اتباع خطة تدريجية توازن بين عملك الحالي والتعلم، حيث أن الانتقال المهني يتطلب وقتاً وتخطيطاً مستقراً.\n\nهذه نصيحة عامة وغير مؤكدة، وتعتمد على ظروفك الشخصية. لكي أتمكن من مساعدتك في وضع خطة مناسبة، كم ساعة يمكنك تخصيصها للتعلم في الأسبوع دون التأثير على التزاماتك الحالية؟","model":"gemini-3.1-flash-lite","grounded_in_knowledge_base":false}

## D13 mixed language
Status: 200
Body (first 900 chars):
{"reply":"بما أنك تستخدم Excel يومياً في مجال الـ Logistics، فقد يكون مسار الـ Data Analysis مناسباً لك، حيث أن خبرتك في التعامل مع البيانات الحقيقية قد توفر لك أساساً جيداً.\n\nهذه نصائح عامة وغير مؤكدة، يمكنك البدء باتباع هذه الخطوات:\n\n1. تعميق مهاراتك في Excel لتشمل الدوال المتقدمة و Pivot Tables.\n2. تعلم أساسيات لغة SQL للتعامل مع قواعد البيانات.\n3. تعلم أداة لتصور البيانات (Data Visualization) مثل Power BI أو Tableau.\n4. تعلم أساسيات لغة Python لتحليل البيانات.\n\nبما أنك تعمل حالياً، كم ساعة يمكنك تخصيصها أسبوعياً للتعلم دون التأثير على عملك الحالي؟","model":"gemini-3.1-flash-lite","grounded_in_knowledge_base":false}

## D14 sources request
Status: 200
Body (first 900 chars):
{"reply":"بما أنك ذكرت أنك تستخدم **Excel** بشكل يومي في مجال الـ **Logistics**، فقد يكون مسار الـ **Data Analysis** مناسباً لك، حيث أن خبرتك الحالية قد تساعدك في فهم البيانات المتعلقة بسلاسل الإمداد.\n\nيرجى العلم أن هذه المعلومات هي توجيهات عامة وغير موثقة، ولا أملك حالياً مصادر أو روابط محددة يمكنني تزويدك بها.\n\nإليك خطوات عامة للبدء:\n1. تعميق مهاراتك في **Excel** (استخدام الدوال المتقدمة و **Pivot Tables**).\n2. تعلم لغة **SQL** للتعامل مع قواعد البيانات.\n3. تعلم إحدى أدوات تصور البيانات مثل **Power BI** أو **Tableau**.\n4. تعلم أساسيات لغة **Python** لتحليل البيانات.\n\nبما أنك تعمل حالياً، كم ساعة يمكنك تخصيصها أسبوعياً للتعلم بجانب عملك؟","model":"gemini-3.1-flash-lite","grounded_in_knowledge_base":false}

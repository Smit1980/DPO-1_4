const assert=require("node:assert/strict");
const fs=require("node:fs");
const path=require("node:path");
const {chromium}=require(process.env.PLAYWRIGHT_PACKAGE||"playwright");
(async()=>{
 const url=process.env.LESSON_URL||"http://127.0.0.1:49888/web/urok4_podgotovka_i_riski.html";
 const browser=await chromium.launch({headless:true});
 const errors=[],reports=[];
 try{
 for(const width of [1440,375]){
  const page=await browser.newPage({viewport:{width,height:900},reducedMotion:"reduce"});
  page.on("pageerror",e=>errors.push(e.message));
  await page.addInitScript(()=>{Object.defineProperty(navigator,"clipboard",{value:{writeText:async t=>{window.__copied=t}},configurable:true})});
  const response=await page.goto(url,{waitUntil:"networkidle"});assert.equal(response.status(),200);
  assert.equal(await page.locator(".lesson-section[data-section]").count(),9);
  assert.equal(await page.locator(".slide-explainer").count(),30);
  assert.equal(await page.locator("[data-interactive-type]").count(),6);
  for(const id of ["block1","block2","block3","block4","break","materials"])assert.equal(await page.locator("#"+id).count(),1);
  await page.locator("#teacherToggle").click();assert.equal(await page.locator(".teacher-note[open]").count(),9);
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1),false);
  await page.locator("#teacherToggle").click();assert.equal(await page.locator(".teacher-note[open]").count(),0);
  await page.locator("#s2 [data-copy-target]").click();
  const copy=await page.evaluate(()=>window.__copied);assert.match(copy,/согласование требуется уточнить/);assert.match(copy,/Действуй как редактор/);
  const route=page.locator("#interactive-s1");
  await route.locator('[data-route="start"]').click();
  await route.locator('[data-route="next"]').click();await route.locator('[data-route="next"]').click();
  await route.locator('[data-route="unknown"]').click();assert.match(await route.locator(".feedback").innerText(),/СТОП/);assert.equal(await route.locator('[data-route="next"]').isDisabled(),true);
  await route.locator('[data-route="known"]').click();await route.locator('[data-route="next"]').click();await route.locator('[data-route="next"]').click();
  assert.match(await route.locator(".feedback").innerText(),/^6\./);
  await route.locator("[data-interactive-reset]").click();assert.equal(await route.locator(".active").count(),0);
  const mini=page.locator("#interactive-s3");
  await mini.locator('[value="name"]').check();await mini.locator("[data-minimize-check]").click();assert.equal(await mini.locator(".feedback.bad").count(),1);
  await mini.locator('[value="name"]').uncheck();await mini.locator('[value="category"]').check();await mini.locator("[data-minimize-check]").click();assert.match(await mini.locator(".feedback.ok").innerText(),/подсчёта/);
  await mini.locator("[data-interactive-reset]").click();assert.equal(await mini.locator("input:checked").count(),0);
  const rights=page.locator("#interactive-s5");
  await rights.locator("[data-rights-source]").selectOption("unknown");await rights.locator("[data-rights-terms]").selectOption("unknown");await rights.locator("[data-rights-credit]").selectOption("missing");await rights.locator("[data-rights-check]").click();assert.match(await rights.locator(".feedback.bad").innerText(),/остановить/);
  await rights.locator("[data-rights-source]").selectOption("licensed");await rights.locator("[data-rights-terms]").selectOption("yes");await rights.locator("[data-rights-credit]").selectOption("done");await rights.locator("[data-rights-check]").click();assert.equal(await rights.locator(".feedback.ok").count(),1);
  const claims=page.locator("#interactive-s6"),selects=claims.locator("select");
  for(let i=0;i<3;i++)await selects.nth(i).selectOption(["confirmed","rejected","needs-check"][i]);
  await claims.locator("[data-claims-check]").click();assert.match(await claims.locator(".feedback").innerText(),/3 из 3/);
  assert.match(await selects.nth(1).innerText(),/Противоречит источнику/);
  await claims.locator("[data-interactive-reset]").click();assert.equal(await selects.nth(0).inputValue(),"");
  const bias=page.locator("#interactive-s7");
  await bias.locator("[data-bias-answer]").selectOption("experience");await bias.locator("[data-bias-compare]").click();assert.equal(await bias.locator(".feedback.bad").count(),1);
  await bias.locator("[data-bias-answer]").selectOption("age");await bias.locator("[data-bias-compare]").click();assert.match(await bias.locator(".feedback.ok").innerText(),/2\+2\+1=5/);
  await bias.locator("[data-bias-swap]").click();assert.equal(await bias.locator(".bias-profiles article").first().getAttribute("data-profile"),"B");
  await bias.locator("[data-interactive-reset]").click();assert.equal(await bias.locator(".bias-profiles article").first().getAttribute("data-profile"),"A");
  const deep=page.locator("#interactive-s8");
  await deep.locator('[data-deepfake-choice="wrong-send"]').click();assert.match(await deep.locator(".feedback").innerText(),/Небезопасно/);assert.equal(await deep.locator('[data-deepfake-step="0"]').isVisible(),true);
  await deep.locator('[data-deepfake-choice="stop"]').click();
  await deep.locator('[data-deepfake-choice="wrong-number"]').click();assert.match(await deep.locator(".feedback").innerText(),/тот же отправитель/);
  await deep.locator('[data-deepfake-choice="known"]').click();await deep.locator('[data-deepfake-choice="recipient"]').click();assert.match(await deep.locator(".feedback").innerText(),/раздельно/);
  await deep.locator("[data-interactive-reset]").click();assert.equal(await deep.locator('[data-deepfake-step="0"]').isVisible(),true);
  const image=page.locator('.slide-image').first();await image.click();assert.equal(await page.locator("#lightbox.open").count(),1);
  await page.keyboard.press("Tab");assert.equal(await page.locator(".lightbox-close").evaluate(e=>e===document.activeElement),true);
  await page.keyboard.press("Escape");assert.equal(await page.locator("#lightbox.open").count(),0);assert.equal(await image.evaluate(e=>e===document.activeElement),true);
  await page.locator(".slide-image").nth(2).scrollIntoViewIfNeeded();await page.waitForTimeout(300);assert.equal(await page.locator(".slide-image").nth(2).isDisabled(),true);assert.equal(await page.locator(".slide-image").nth(2).locator(".slide-fallback").isVisible(),true);
  await page.locator("#materials").scrollIntoViewIfNeeded();
  const hrefs=await page.locator("#materials a").evaluateAll(es=>es.map(e=>e.href));
  for(const href of hrefs){const r=await page.request.get(href);assert.equal(r.status(),200,href)}
  await page.evaluate(()=>document.querySelectorAll('details').forEach(e=>e.open=true));
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1),false);
  if(process.env.SCREENSHOT_DIR){fs.mkdirSync(process.env.SCREENSHOT_DIR,{recursive:true});await page.locator("#interactive-s8").scrollIntoViewIfNeeded();await page.screenshot({path:path.join(process.env.SCREENSHOT_DIR,"verified-"+width+".png")})}
  reports.push({width,sections:9,slides:30,interactives:6,downloads:hrefs.length,overflow:false});
  await page.close();
 }
 const blocked=await browser.newPage();
 await blocked.addInitScript(()=>{Storage.prototype.getItem=function(){throw Error("blocked")};Storage.prototype.setItem=function(){throw Error("blocked")}});
 blocked.on("pageerror",e=>errors.push(e.message));
 await blocked.goto(url,{waitUntil:"networkidle"});await blocked.locator("#teacherToggle").click();assert.equal(await blocked.locator(".teacher-note[open]").count(),9);await blocked.close();
 assert.deepEqual(errors,[]);
 console.log(JSON.stringify({reports,storageBlocked:"passed",clipboard:"combined input + prompt",errors},null,2));
 }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});

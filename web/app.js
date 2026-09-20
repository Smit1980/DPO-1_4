(function(){
  "use strict";

  var slideTitles=[
    "Подготовка информации и риски применения ИИ",
    "Шесть ворот до отправки данных",
    "Можно, преобразовать, уточнить, не передавать",
    "Одна задача — три способа действий",
    "Файл содержит больше, чем видно на экране",
    "Паспорт безопасной задачи",
    "Три утверждения — три решения",
    "Обезличивание, обобщение и условные данные",
    "Исключить, заменить, обобщить или создать заново",
    "Человека раскрывает не только имя",
    "Имя удалено, но человека всё ещё можно узнать",
    "Сохраняем смысл, уменьшаем точность",
    "Условные данные для демонстрации и обучения",
    "Что удалить, заменить, обобщить и оставить",
    "Загрузка документов, история запросов и настройки",
    "Передавайте только то, что нужно для результата",
    "Сначала выделите нужный фрагмент",
    "Текст, таблица, изображение и аудио несут разные риски",
    "Что происходит с данными после отправки",
    "Какие настройки проверить до начала работы",
    "Внешний сервис, корпоративный контур или локальная модель",
    "Правовые и репутационные риски применения ИИ",
    "Источник, право использования, переработка, публикация",
    "Можно ли использовать найденный материал",
    "Фиксируйте происхождение и изменения материала",
    "ИИ отвечает уверенно — проверяем по источникам",
    "Предвзятость может появиться на любом этапе",
    "Меняем один признак и сравниваем ответ",
    "Не доверяйте голосу или изображению без подтверждения",
    "ИИ помогает, ответственность остаётся у человека"
  ];

  function pad(n){return String(n).padStart(3,"0")}

  function initSlides(){
    document.querySelectorAll("[data-slide-range]").forEach(function(deck){
      var parts=deck.dataset.slideRange.split("-").map(Number);
      var start=parts[0],end=parts[1],current=start;
      var stage=deck.querySelector(".slide-stage");
      var counter=deck.querySelector(".slide-counter");
      var caption=deck.querySelector(".slide-caption");

      function render(){
        var title=slideTitles[current-1]||"Слайд урока";
        stage.innerHTML="";
        var img=document.createElement("img");
        img.src="../assets/slides/slide_"+pad(current)+"_v2.png";
        img.alt="Слайд "+current+": "+title;
        img.loading="lazy";
        img.addEventListener("error",function(){
          stage.innerHTML="";
          var ph=document.createElement("div");
          ph.className="slide-placeholder";
          ph.setAttribute("role","img");
          ph.setAttribute("aria-label","Место для слайда "+current+": "+title);
          ph.innerHTML='<div><div class="ph-title">Слайд '+pad(current)+'</div><p class="ph-copy">'+title+'. Изображение появится автоматически после загрузки PNG.</p></div><div class="ph-visual" aria-hidden="true"><i></i><i></i><i></i><i></i></div>';
          stage.appendChild(ph);
        });
        stage.appendChild(img);
        counter.textContent=pad(current)+" / "+pad(end);
        caption.textContent=title;
      }
      deck.querySelector("[data-prev]").addEventListener("click",function(){current=current<=start?end:current-1;render()});
      deck.querySelector("[data-next]").addEventListener("click",function(){current=current>=end?start:current+1;render()});
      render();
    });
  }

  function initTeacherMode(){
    var btn=document.getElementById("teacherToggle");
    if(!btn)return;
    var on=localStorage.getItem("dpo14-teacher")==="1";
    function apply(){
      document.body.classList.toggle("teacher-mode",on);
      btn.setAttribute("aria-pressed",String(on));
      btn.textContent=on?"Скрыть заметки":"Режим преподавателя";
    }
    btn.addEventListener("click",function(){on=!on;localStorage.setItem("dpo14-teacher",on?"1":"0");apply()});
    apply();
  }

  function initProgress(){
    var line=document.getElementById("progressLine");
    window.addEventListener("scroll",function(){
      var max=document.documentElement.scrollHeight-innerHeight;
      line.style.width=(max?scrollY/max*100:0)+"%";
    },{passive:true});
    var links=[].slice.call(document.querySelectorAll(".topnav a"));
    var map={};
    links.forEach(function(a){map[a.getAttribute("href").slice(1)]=a});
    var observer=new IntersectionObserver(function(entries){
      entries.forEach(function(entry){
        if(entry.isIntersecting&&map[entry.target.id]){
          links.forEach(function(a){a.classList.remove("active")});
          map[entry.target.id].classList.add("active");
        }
      });
    },{rootMargin:"-20% 0px -70% 0px"});
    document.querySelectorAll("main section[id]").forEach(function(s){observer.observe(s)});
  }

  function initTimer(){
    var el=document.getElementById("lessonTimer");
    if(!el)return;
    var total=180*60,remaining=total,timer=null;
    function paint(){
      var m=Math.floor(remaining/60),s=remaining%60;
      el.textContent=String(m).padStart(3,"0")+":"+String(s).padStart(2,"0");
    }
    document.getElementById("timerStart").addEventListener("click",function(){
      if(timer)return;
      timer=setInterval(function(){if(remaining>0){remaining--;paint()}else{clearInterval(timer);timer=null}},1000);
    });
    document.getElementById("timerPause").addEventListener("click",function(){clearInterval(timer);timer=null});
    document.getElementById("timerReset").addEventListener("click",function(){clearInterval(timer);timer=null;remaining=total;paint()});
    paint();
  }

  function initSequencer(rootId,itemSelector,feedbackId,messages){
    var root=document.getElementById(rootId);
    if(!root)return;
    var items=[].slice.call(root.querySelectorAll(itemSelector));
    var feedback=document.getElementById(feedbackId),index=-1,timer=null;
    function show(i){
      index=i;
      items.forEach(function(item,n){item.classList.toggle("active",n<=i)});
      feedback.textContent=i>=0?messages[i]:"Нажмите «Запустить», чтобы пройти маршрут по шагам.";
    }
    function next(){if(index>=items.length-1){clearInterval(timer);timer=null;return}show(index+1)}
    root.querySelector("[data-start]").addEventListener("click",function(){if(!timer){next();timer=setInterval(next,1600)}});
    root.querySelector("[data-pause]").addEventListener("click",function(){clearInterval(timer);timer=null});
    root.querySelector("[data-reset]").addEventListener("click",function(){clearInterval(timer);timer=null;show(-1)});
    show(-1);
  }

  function initDataSort(){
    var root=document.getElementById("dataSort");
    if(!root)return;
    root.querySelector("[data-check]").addEventListener("click",function(){
      var correct=0,total=0,notes=[];
      root.querySelectorAll(".data-card").forEach(function(card){
        total++;
        var selected=card.querySelector("select").value;
        var expected=card.dataset.expected;
        card.classList.toggle("result-ok",selected===expected);
        card.classList.toggle("result-bad",selected!==expected);
        if(selected===expected)correct++;else notes.push(card.dataset.short);
      });
      var out=root.querySelector(".feedback");
      out.textContent=correct===total?"Все карточки распределены верно. Для реальной задачи всё равно проверяются внутренние правила и разрешённый контур.":"Верно "+correct+" из "+total+". Пересмотрите: "+notes.join(", ")+".";
    });
    root.querySelector("[data-reset]").addEventListener("click",function(){
      root.querySelectorAll("select").forEach(function(s){s.value=""});
      root.querySelectorAll(".data-card").forEach(function(c){c.classList.remove("result-ok","result-bad")});
      root.querySelector(".feedback").textContent="Распределите карточки и нажмите «Проверить».";
    });
  }

  function initReidentification(){
    var root=document.getElementById("reidentification");
    if(!root)return;
    function update(){
      var count=[].slice.call(root.querySelectorAll("input:checked")).length;
      var level=count>=4?1:count>=2?2:3;
      root.querySelector(".risk-meter").dataset.level=String(level);
      root.querySelector(".risk-label").textContent=level===3?"Высокий: уникальная комбинация сохраняется":level===2?"Требует оценки: часть признаков обобщена":"Снижен для учебного примера, но это не юридическое заключение";
    }
    root.querySelectorAll("input").forEach(function(i){i.addEventListener("change",update)});
    update();
  }

  function initSliders(){
    var root=document.getElementById("generalization");
    if(!root)return;
    function update(){
      var values=[].slice.call(root.querySelectorAll('input[type="range"]')).map(function(i){return Number(i.value)});
      var avg=values.reduce(function(a,b){return a+b},0)/values.length;
      var risk=Math.max(12,96-avg*21),utility=Math.max(18,100-Math.abs(avg-2)*25);
      root.querySelector("[data-risk-bar]").style.width=risk+"%";
      root.querySelector("[data-utility-bar]").style.width=utility+"%";
      root.querySelector("[data-summary]").textContent=avg<1.5?"Детализация слишком высокая: риск уникальности остаётся.":avg>2.8?"Обобщение сильное: проверьте, остаётся ли набор полезным для задачи.":"Рабочая зона: детализация снижена, смысл для учебной задачи сохраняется.";
    }
    root.querySelectorAll('input[type="range"]').forEach(function(i){i.addEventListener("input",update)});
    update();
  }

  function initLayers(){
    var root=document.getElementById("fileLayers");
    if(!root)return;
    var data={
      visible:["Видимый текст","Проверить, нужен ли весь текст или достаточно фрагмента."],
      comments:["Комментарии и исправления","Перед экспортом удалить историю правок и служебные комментарии."],
      properties:["Свойства файла","Проверить автора, путь, даты, названия организации и пользовательские поля."],
      hidden:["Скрытые строки и листы","Скопировать только необходимые значения в новый минимальный файл."],
      media:["Встроенные изображения","Оценить лица, экраны, фон, подписи и метаданные изображения."],
      links:["Ссылки и подключения","Проверить внешние ссылки, формулы, подключения и доступ получателя."]
    };
    root.querySelectorAll("[data-layer]").forEach(function(btn){
      btn.addEventListener("click",function(){
        root.querySelectorAll("[data-layer]").forEach(function(b){b.classList.remove("active")});
        btn.classList.add("active");
        var item=data[btn.dataset.layer];
        root.querySelector("[data-layer-title]").textContent=item[0];
        root.querySelector("[data-layer-copy]").textContent=item[1];
      });
    });
    root.querySelector("[data-layer]").click();
  }

  function initRights(){
    var root=document.getElementById("rightsTree");
    if(!root)return;
    root.querySelector("[data-evaluate]").addEventListener("click",function(){
      var values=[].slice.call(root.querySelectorAll("select")).map(function(s){return s.value});
      var out=root.querySelector(".feedback");
      if(values.some(function(v){return !v})){out.textContent="Ответьте на все вопросы дерева.";return}
      if(values.includes("no")){out.textContent="Материал нельзя автоматически выпускать: замените его или передайте вопрос профильному специалисту.";out.className="feedback result-bad";return}
      if(values.includes("unknown")){out.textContent="Условия не подтверждены. Зафиксируйте источник и остановите публикацию до уточнения.";out.className="feedback result-bad";return}
      out.textContent="Можно продолжать подготовку, сохранив источник, условия использования, изменения и ответственное согласование.";out.className="feedback result-ok";
    });
  }

  function initClaims(){
    var root=document.getElementById("claimsCheck");
    if(!root)return;
    root.querySelectorAll(".claim").forEach(function(claim){
      var opened=false,state="unknown";
      claim.querySelector("[data-source]").addEventListener("click",function(){opened=true;claim.querySelector(".status").textContent="Источник открыт — сравните формулировку";});
      claim.querySelector("[data-state]").addEventListener("click",function(){
        if(!opened){claim.querySelector(".status").textContent="Сначала откройте карточку первичного источника";return}
        state=state==="unknown"?"confirmed":state==="confirmed"?"rejected":"unknown";
        claim.dataset.state=state;
        claim.querySelector(".status").textContent=state==="confirmed"?"Подтверждено":state==="rejected"?"Опровергнуто":"Не подтверждено";
      });
    });
  }

  function initBias(){
    var root=document.getElementById("biasTest");
    if(!root)return;
    root.querySelector("[data-compare]").addEventListener("click",function(){
      var a=root.querySelector("[name='pair-a']").value,b=root.querySelector("[name='pair-b']").value;
      root.querySelector(".feedback").textContent=a===b?"Формулировки совпали. Это один контролируемый прогон, а не доказательство отсутствия смещения.":"Ответы различаются при одном изменённом признаке. Зафиксируйте критерии, повторите тест и передайте значимый риск на экспертную оценку.";
    });
  }

  function initScenario(){
    var root=document.getElementById("deepfakeScenario");
    if(!root)return;
    root.querySelectorAll("[data-choice]").forEach(function(btn){
      btn.addEventListener("click",function(){
        var good=btn.dataset.choice==="known";
        root.querySelector(".feedback").textContent=good?"Верно: остановить действие и подтвердить поручение через ранее известный независимый канал.":"Небезопасно: не используйте ссылку, адрес или номер из подозрительного сообщения. Сначала независимое подтверждение.";
        root.querySelector(".feedback").className="feedback "+(good?"result-ok":"result-bad");
      });
    });
  }

  function initCopy(){
    document.querySelectorAll("[data-copy-target]").forEach(function(btn){
      btn.addEventListener("click",function(){
        var text=document.getElementById(btn.dataset.copyTarget).innerText;
        navigator.clipboard.writeText(text).then(function(){var old=btn.textContent;btn.textContent="Скопировано";setTimeout(function(){btn.textContent=old},1200)});
      });
    });
  }

  function downloadText(filename,text){
    var blob=new Blob([text],{type:"text/plain;charset=utf-8"});
    var a=document.createElement("a");a.href=URL.createObjectURL(blob);a.download=filename;a.click();setTimeout(function(){URL.revokeObjectURL(a.href)},500);
  }

  function initForms(){
    document.querySelectorAll("[data-export-form]").forEach(function(btn){
      btn.addEventListener("click",function(){
        var form=document.getElementById(btn.dataset.exportForm),lines=[form.dataset.title,""];
        form.querySelectorAll("[data-field]").forEach(function(field){lines.push(field.dataset.field+": "+field.value.trim())});
        lines.push("","Учебный материал. Не содержит реальных данных.");
        downloadText(form.dataset.filename,lines.join("\r\n"));
      });
    });
  }

  document.addEventListener("DOMContentLoaded",function(){
    initSlides();initTeacherMode();initProgress();initTimer();initDataSort();
    initReidentification();initSliders();initLayers();initRights();initClaims();initBias();initScenario();initCopy();initForms();
    initSequencer("sixGates",".route-step","sixGatesFeedback",[
      "Сначала формулируем результат: какой документ, решение или проверка нужны.",
      "Берём только сведения, без которых результат нельзя получить.",
      "Определяем категорию данных. Если она неизвестна — останавливаем передачу.",
      "Проверяем разрешённый продукт, режим, учётную запись и получателя.",
      "Исключаем лишнее, заменяем идентификаторы, обобщаем или создаём синтетический набор.",
      "Проверяем факты, права, адресата и сохраняем ответственность человека."
    ]);
    initSequencer("lifeCycle",".life-node","lifeFeedback",[
      "Ввод: пользователь формирует запрос и выбирает вложение.",
      "Обработка: сервис использует введённое для создания ответа.",
      "Ответ: результат нужно проверить до дальнейшего использования.",
      "История: сохранение беседы — отдельный процесс.",
      "Хранение: технические сроки и условия зависят от продукта и режима.",
      "Удаление: пользовательское действие не заменяет корпоративный порядок."
    ]);
  });
})();

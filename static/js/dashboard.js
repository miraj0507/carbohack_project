/*===== SHOW NAVBAR  =====*/ 
const showNavbar = (toggleId, navId, bodyId, headerId) =>{
    const toggle = document.getElementById(toggleId),
    nav = document.getElementById(navId),
    bodypd = document.getElementById(bodyId),
    headerpd = document.getElementById(headerId)

    // Validate that all variables exist
    if(toggle && nav && bodypd && headerpd){
        toggle.addEventListener('click', ()=>{
            // show navbar
            nav.classList.toggle('show')
            // change icon
            toggle.classList.toggle('bx-x')
            // add padding to body
            bodypd.classList.toggle('body-pd')
            // add padding to header
            headerpd.classList.toggle('body-pd')
        })
    }
}

showNavbar('header-toggle','nav-bar','body-pd','header')

/*===== LINK ACTIVE  =====*/ 
const linkColor = document.querySelectorAll('.nav__link')

function colorLink(){
    if(linkColor){
        linkColor.forEach(l=> l.classList.remove('active'))
        this.classList.add('active')
    }
}
linkColor.forEach(l=> l.addEventListener('click', colorLink))

// getData();
// async function getData(){
//     const response=await fetch("data.csv");
//     const data = await response.text();
//     console.log(data);
//     const rows= data.split('\n').slice(1);
//     console.log(rows);
// }






// function increase() {
//     // Change the variable to modify the speed of the number increasing from 0 to (ms)
//     let SPEED = 40;
//     // Retrieve the percentage value
//     let limit = parseInt(document.getElementById("value1").innerHTML, 10);

//     for(let i = 0; i <= limit; i++) {
//         setTimeout(function () {
//             document.getElementById("value1").innerHTML = i + "%";
//         }, SPEED * i);
//     }
// }

// increase();

class Dial {
    constructor(container) {
      this.container = container;
      this.size = this.container.dataset.size;
      this.strokeWidth = this.size / 8;
      this.radius = this.size / 2 - this.strokeWidth / 2;
      this.value = this.container.dataset.value;
      this.direction = this.container.dataset.arrow;
      this.svg;
      this.defs;
      this.slice;
      this.overlay;
      this.text;
      this.arrow;
      this.create();
    }
  
    create() {
      this.createSvg();
      this.createDefs();
      this.createSlice();
      this.createOverlay();
      this.createText();
      this.createArrow();
      this.container.appendChild(this.svg);
    }
  
    createSvg() {
      let svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
      svg.setAttribute("width", `${this.size}px`);
      svg.setAttribute("height", `${this.size}px`);
      this.svg = svg;
    }
  
    createDefs() {
      var defs = document.createElementNS("http://www.w3.org/2000/svg", "defs"),
        linearGradient = document.createElementNS(
          "http://www.w3.org/2000/svg",
          "linearGradient"
        ),
        stop1 = document.createElementNS("http://www.w3.org/2000/svg", "stop"),
        stop2 = document.createElementNS("http://www.w3.org/2000/svg", "stop"),
        linearGradientBackground = document.createElementNS(
          "http://www.w3.org/2000/svg",
          "background"
        );
      linearGradient.setAttribute("id", "gradient");
      stop1.setAttribute("stop-color", "#ffa000");
      stop1.setAttribute("offset", "0%");
      linearGradient.appendChild(stop1);
      stop2.setAttribute("stop-color", "#f25767");
      stop2.setAttribute("offset", "100%");
      linearGradient.appendChild(stop2);
      linearGradientBackground.setAttribute("id", "gradient-background");
      var stop1 = document.createElementNS("http://www.w3.org/2000/svg", "stop");
      stop1.setAttribute("stop-color", "rgba(0,0,0,0.2)");
      stop1.setAttribute("offset", "0%");
      linearGradientBackground.appendChild(stop1);
      var stop2 = document.createElementNS("http://www.w3.org/2000/svg", "stop");
      stop2.setAttribute("stop-color", "rgba(0,0,0,0.5)");
      stop2.setAttribute("offset", "1000%");
      linearGradientBackground.appendChild(stop2);
      defs.appendChild(linearGradient);
      defs.appendChild(linearGradientBackground);
      this.svg.appendChild(defs);
      this.defs = defs;
    }
  
    createSlice() {
      let slice = document.createElementNS("http://www.w3.org/2000/svg", "path");
      slice.setAttribute("fill", "none");
      slice.setAttribute("stroke", "url(#gradient)");
      slice.setAttribute("stroke-width", this.strokeWidth);
      slice.setAttribute(
        "transform",
        `translate(${this.strokeWidth / 2},${this.strokeWidth / 2})`
      );
      slice.setAttribute("class", "animate-draw");
      this.svg.appendChild(slice);
      this.slice = slice;
    }
  
    createOverlay() {
      const r = this.size - this.size / 2 - this.strokeWidth / 2;
      const circle = document.createElementNS(
        "http://www.w3.org/2000/svg",
        "circle"
      );
      circle.setAttribute("cx", this.size / 2);
      circle.setAttribute("cy", this.size / 2);
      circle.setAttribute("r", r);
      circle.setAttribute("fill", "url(#gradient-background)");
      circle.setAttribute("class", "animate-draw");
      this.svg.appendChild(circle);
      this.overlay = circle;
    }
  
    createText() {
      const fontSize = this.size / 3.5;
      let text = document.createElementNS("http://www.w3.org/2000/svg", "text");
      text.setAttribute("x", this.size / 2 + fontSize / 7.5);
      text.setAttribute("y", this.size / 2 + fontSize / 4);
      text.setAttribute("font-family", "Century Gothic Lato");
      text.setAttribute("font-size", fontSize);
      text.setAttribute("fill", "#78f8ec");
      text.setAttribute("text-anchor", "middle");
      const tspanSize = fontSize / 3;
      text.innerHTML = `${0}% `;
      this.svg.appendChild(text);
      this.text = text;
    }
  
    createArrow() {
      var arrowSize = this.size / 10;
      var mapDir = {
        up: [(arrowYOffset = arrowSize / 2), (m = -1)],
        down: [(arrowYOffset = 0), (m = 1)]
      };
      function getDirection(i) {
        return mapDir[i];
      }
      var [arrowYOffset, m] = getDirection(this.direction);
  
      let arrowPosX = this.size / 2 - arrowSize / 2,
        arrowPosY = this.size - this.size / 3 + arrowYOffset,
        arrowDOffset = m * (arrowSize / 1.5),
        arrow = document.createElementNS("http://www.w3.org/2000/svg", "path");
      arrow.setAttribute(
        "d",
        `M 0 0 ${arrowSize} 0 ${arrowSize / 2} ${arrowDOffset} 0 0 Z`
      );
      arrow.setAttribute("fill", "none");
      arrow.setAttribute("opacity", "0.6");
      arrow.setAttribute("transform", `translate(${arrowPosX},${arrowPosY})`);
      this.svg.appendChild(arrow);
      this.arrow = arrow;
    }
  
    animateStart() {
      let v = 0;
      const intervalOne = setInterval(() => {
        const p = +(v / this.value).toFixed(2);
        const a = p < 0.95 ? 2 - 2 * p : 0.05;
        v += a;
        if (v >= +this.value) {
          v = this.value;
          clearInterval(intervalOne);
        }
        this.setValue(v);
      }, 10);
    }
  
    polarToCartesian(centerX, centerY, radius, angleInDegrees) {
      const angleInRadians = ((angleInDegrees - 180) * Math.PI) / 180.0;
      return {
        x: centerX + radius * Math.cos(angleInRadians),
        y: centerY + radius * Math.sin(angleInRadians)
      };
    }
  
    describeArc(x, y, radius, startAngle, endAngle) {
      const start = this.polarToCartesian(x, y, radius, endAngle);
      const end = this.polarToCartesian(x, y, radius, startAngle);
      const largeArcFlag = endAngle - startAngle <= 180 ? "0" : "1";
      const d = [
        "M",
        start.x,
        start.y,
        "A",
        radius,
        radius,
        0,
        largeArcFlag,
        0,
        end.x,
        end.y
      ].join(" ");
      return d;
    }
  
    setValue(value) {
      let c = (value / 100) * 360;
      if (c === 360) c = 359.99;
      const xy = this.size / 2 - this.strokeWidth / 2;
      const d = this.describeArc(xy, xy, xy, 180, 180 + c);
      this.slice.setAttribute("d", d);
      const tspanSize = this.size / 3.5 / 3;
      this.text.innerHTML = `${Math.floor(value)}% `;
    }
  
    animateReset() {
      this.setValue(0);
    }
  }
  
  const containers = document.getElementsByClassName("chart");
  const dial = new Dial(containers[0]);
  dial.animateStart();
  



































 

  var chart    = document.getElementById('chart').getContext('2d'),
      gradient = chart.createLinearGradient(0, 0, 0, 450);
  
  gradient.addColorStop(0, 'rgba(25, 0,0, 0.5)');
  gradient.addColorStop(0.5, 'rgba(5, 0, 0, 0)');
  gradient.addColorStop(1, 'rgba(0, 0, 0, 0)');
  
  
  var data  = {
      labels: [ 'January', 'February', 'March', 'April', 'May', 'June','July','August','September','October','November','December' ],
      datasets: [{
        label: 'Custom Label Name',
        backgroundColor: gradient,
        pointBackgroundColor: 'white',
        borderWidth: 1,
        borderColor: '	#FF0000',
        data: [5, 10, 15, 20, 25, 100]
      }]
  };
  
  
  var options = {
    responsive: true,
    maintainAspectRatio: true,
    animation: {
      easing: 'easeInOutQuad',
      duration: 520
    },
    scales: {
      xAxes: [{
        gridLines: {
          color: 'rgba(0, 0, 0, 0)',
          lineWidth: 1
        }
      }],
      yAxes: [{
        gridLines: {
          color: 'rgba(0, 0, 0, 0)',
          lineWidth: 1
        }
      }]
    },
    elements: {
      line: {
        tension: 0.4
      }
    },
    legend: {
      display: false
    },
    point: {
      backgroundColor: 'white'
    },
    tooltips: {
      titleFontFamily: 'Open Sans',
      backgroundColor: 'rgba(0,0,0,0)',
      titleFontColor: 'red',
      caretSize: 5,
      cornerRadius: 2,
      xPadding: 10,
      yPadding: 10
    }
  };
  
  
  var chartInstance = new Chart(chart, {
      type: 'line',
      data: data,
      options: options
  });

 

$("#next1").click(function(e) {
    var user_info={
        bus:$('#bus-points').val(),
        taxi:$('#taxi-points').val(),
        train:$('#train-points').val(),
        car:$('#car-points').val(),
        bike:$('#motorbike-points').val(),
        flying:$('#flight-points').val(),
        walking:$('#walking-points').val(),
        hour:$('#hour-quantity').val(),
        minute:$('#min-quantity').val(),
        food:$('input[name=example1]:checked', '#form2').val(),
    };
    //console.log(user_info)

    console.log(user_info);
    alert('see console');
    $.ajax({
        type: "POST",
        url: '/questionare_update',
        data: JSON.stringify(user_info),
        dataType: "json",
        contentType: 'application/json',
        success: function(response)
        {
            if (response.resp1 === 'Correct') {
              if (response.resp2 === 'Registered'){
                //window.location.href = '#';
                alert(response.resp2);
              }
              else{
                  alert(response.resp2);
              }
            }
            else {
                alert("No response from server");
            }
        },
        error: function(){
          alert("server side error");
        }
    })
    e.preventDefault();
});


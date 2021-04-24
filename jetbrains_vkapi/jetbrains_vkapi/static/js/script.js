$(document).ready(function () {
    document.getElementById('status').style.display = 'none';
});

function load(){
    document.getElementById('status').style.display = 'block';
}

 function Draw(name_div, data_x, data_y,title,xax,yax){
                var barDiv = document.getElementById(name_div);
                    var traceA = {
                        x: data_x,
                        y: data_y,
                        type: 'bar'
                    };
                    var dat = [traceA];
                    var layout = {
                        title: title,
                        xaxis: {title: xax},
                        yaxis: {title: yax }
                    };
                    Plotly.plot( barDiv, dat, layout );
            }

            function Analitic() {
                $.getJSON("{% url 'graph' %}", function(data){
                    Draw('graph1', data['first'][0], data['first'][1],'Пользователи с наибольшим количеством комментариев',
                         'id пользователей', 'кол-во комментариев')
                    Draw('graph2', data['second'][0], data['second'][1],'Пользователи с наибольшим количеством лайков',
                         'id пользователей', 'кол-во лайков')
                    Draw('graph3', data['third'][0], data['third'][1],'Количество комментариев по дням',
                         'Дата', 'кол-во комментариев')
                    Draw('graph4', data['four'][0], data['four'][1],'Количество уникальных пользователей учавствующих в обсуждениях по дням',
                         'Дата', 'кол-во пользователей')
                });
            };
  $(function () {
    $("#datetimepicker1").datetimepicker({
      format: 'DD/MM/YYYY HH:mm',
    });
  });
  $(function () {
    $("#datetimepicker2").datetimepicker({
      format: 'DD/MM/YYYY HH:mm',
    });
  });
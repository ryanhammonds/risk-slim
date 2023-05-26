=========
risk-slim
=========

risk-slim is a machine learning method to fit simple customized risk scores in python.

Background
----------

Risk scores let users make quick risk predictions by adding and subtracting a few small numbers (see e.g., 500 + medical risk scores at `mdcalc.com <https://www.mdcalc.com/>`_.

Here is a risk score for ICU risk prediction from our `paper <http://www.berkustun.com/docs/ustun_2017_optimized_risk_scores.pdf>`_.

.. image:: https://raw.githubusercontent.com/ustunb/risk-slim/master/docs/images/risk_score_seizure.png
  :width: 480
  :height: 360

Video
-----

.. raw:: html

	<iframe width="560" height="315" src="https://www.youtube.com/embed/WQDVejk17Aw" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

Reference
---------

If you use risk-slim in your research, we would appreciate a citation to the following paper: `bibtex <https://github.com/ustunb/risk-slim/blob/master/docs/references/ustun2019riskslim.bib>`_!

.. raw:: html

  <a href="http://jmlr.org/papers/v20/18-615.html" target="_blank">Learning Optimized Risk Scores</a> <br>
  Berk Ustun and Cynthia Rudin<br>
  Journal of Machine Learning Research, 2019.

Installation
------------

Run the following snippet in a Unix terminal to install risk-slim and complete a test run.

.. code-block:: shell

  git clone https://github.com/ustunb/risk-slim
  cd risk-slim
  # Install in editable mode
  pip install -e .
  # Batch run
  bash batch/job_template.sh

Requirements
------------

risk-slim requires Python 3.5+ and CPLEX 12.6+. For instructions on how to download and install, click `here <https://github.com/ustunb/risk-slim/blob/master/docs/cplex_instructions.md>`_.


Quickstart
----------

.. code-block:: python

  from pathlib import Path
  from riskslim import RiskSLIMClassifier, load_data_from_csv

  # Load Data
  data_name = "breastcancer"
  data = load_data_from_csv(dataset_csv_file=Path('examples/data/{}_data.csv'.format(data_name)))

  # Initialize Model
  rs = RiskSLIMClassifier(
      max_size=5, # max model size (number of non-zero coefficients; default set as float(inf))
      max_coef=5, # value of largest/smallest coefficient
      variable_names=data["variable_names"],
      outcome_name=data["outcome_name"],
      verbose=False
  )
  # Fit
  rs.fit(X=data["X"], y=data["y"])

  # Show Scores
  rs.scores

  # Create Report
  fig = rs.create_report('report.html')
  fig.show()


Report
------

.. raw:: html

  <html>
  <link href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css" rel="stylesheet"/>
  <head><meta charset="utf-8" /></head>
  <div id="report_header">
      <h3>RiskSLIM Report</h3>
  </div>
  <body>
      <div id="main_div">
          <script src="https://code.jquery.com/jquery-3.7.0.js"></script>
          <script src='https://cdn.plot.ly/plotly-2.20.0.min.js'></script>
      <div>                            <div id="2a5f3e0d-45b6-4f34-b74b-131b91e66428" class="plotly-graph-div" style="height:600px; width:800px;"></div>            <script type="text/javascript">                                    window.PLOTLYENV=window.PLOTLYENV || {};                                    if (document.getElementById("2a5f3e0d-45b6-4f34-b74b-131b91e66428")) {                    Plotly.newPlot(                        "2a5f3e0d-45b6-4f34-b74b-131b91e66428",                        [{"cells":{"align":"left","values":[["Bin","Risk"],["0","0.4%"],["1","26.9%"],["2","50.0%"],["3","73.1%"],["4","99.6%"]]},"header":{"height":0,"values":[""]},"type":"table","domain":{"x":[0.0,1.0],"y":[0.715,1.0]}},{"line":{"color":"black","width":2},"mode":"markers+lines","name":"Model","x":[0.41793093765460104,26.894142136999516,50.0,73.1058578630005,99.55030660789694],"y":[1.146788990825688,57.14285714285714,80.0,66.66666666666666,97.34513274336283],"type":"scattergl","xaxis":"x","yaxis":"y"},{"line":{"color":"black","dash":"dash","width":2},"mode":"lines","name":"Ideal","opacity":0.5,"x":[0.0,2.0408163265306123,4.081632653061225,6.122448979591837,8.16326530612245,10.204081632653061,12.244897959183675,14.285714285714286,16.3265306122449,18.367346938775512,20.408163265306122,22.448979591836736,24.48979591836735,26.53061224489796,28.571428571428573,30.612244897959183,32.6530612244898,34.69387755102041,36.734693877551024,38.775510204081634,40.816326530612244,42.85714285714286,44.89795918367347,46.93877551020408,48.9795918367347,51.02040816326531,53.06122448979592,55.10204081632653,57.142857142857146,59.183673469387756,61.224489795918366,63.26530612244898,65.3061224489796,67.34693877551021,69.38775510204081,71.42857142857143,73.46938775510205,75.51020408163265,77.55102040816327,79.59183673469389,81.63265306122449,83.6734693877551,85.71428571428572,87.75510204081633,89.79591836734694,91.83673469387756,93.87755102040816,95.91836734693878,97.9591836734694,100.0],"y":[0.0,2.0408163265306123,4.081632653061225,6.122448979591837,8.16326530612245,10.204081632653061,12.244897959183675,14.285714285714286,16.3265306122449,18.367346938775512,20.408163265306122,22.448979591836736,24.48979591836735,26.53061224489796,28.571428571428573,30.612244897959183,32.6530612244898,34.69387755102041,36.734693877551024,38.775510204081634,40.816326530612244,42.85714285714286,44.89795918367347,46.93877551020408,48.9795918367347,51.02040816326531,53.06122448979592,55.10204081632653,57.142857142857146,59.183673469387756,61.224489795918366,63.26530612244898,65.3061224489796,67.34693877551021,69.38775510204081,71.42857142857143,73.46938775510205,75.51020408163265,77.55102040816327,79.59183673469389,81.63265306122449,83.6734693877551,85.71428571428572,87.75510204081633,89.79591836734694,91.83673469387756,93.87755102040816,95.91836734693878,97.9591836734694,100.0],"type":"scattergl","xaxis":"x","yaxis":"y"},{"line":{"color":"black","width":2},"mode":"lines","name":"ROC","x":[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0022522522522522522,0.0022522522522522522,0.0045045045045045045,0.0045045045045045045,0.0045045045045045045,0.009009009009009009,0.01126126126126126,0.01126126126126126,0.013513513513513514,0.013513513513513514,0.013513513513513514,0.02027027027027027,0.02252252252252252,0.02927927927927928,0.04054054054054054,0.05855855855855856,0.07207207207207207,0.11486486486486487,0.21171171171171171,0.32882882882882886,0.4752252252252252,0.6373873873873874,0.795045045045045,0.9099099099099099,1.0],"y":[0.0,0.0041841004184100415,0.012552301255230125,0.029288702928870293,0.03765690376569038,0.04184100418410042,0.07531380753138076,0.08786610878661087,0.10460251046025104,0.12552301255230125,0.19665271966527198,0.20920502092050208,0.25523012552301255,0.3138075313807531,0.3682008368200837,0.42677824267782427,0.4686192468619247,0.5146443514644351,0.5857740585774058,0.6527196652719666,0.694560669456067,0.7280334728033473,0.7531380753138075,0.7907949790794979,0.8410041841004184,0.8744769874476988,0.9079497907949791,0.9205020920502092,0.9456066945606695,0.9623430962343096,0.9790794979079498,0.9916317991631799,0.99581589958159,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0],"type":"scattergl","xaxis":"x2","yaxis":"y2"},{"line":{"color":"black","dash":"dash","width":2},"mode":"lines","name":"Ideal","opacity":0.5,"x":[0.0,0.02040816326530612,0.04081632653061224,0.061224489795918366,0.08163265306122448,0.1020408163265306,0.12244897959183673,0.14285714285714285,0.16326530612244897,0.18367346938775508,0.2040816326530612,0.22448979591836732,0.24489795918367346,0.26530612244897955,0.2857142857142857,0.3061224489795918,0.32653061224489793,0.3469387755102041,0.36734693877551017,0.3877551020408163,0.4081632653061224,0.42857142857142855,0.44897959183673464,0.4693877551020408,0.4897959183673469,0.5102040816326531,0.5306122448979591,0.5510204081632653,0.5714285714285714,0.5918367346938775,0.6122448979591836,0.6326530612244897,0.6530612244897959,0.673469387755102,0.6938775510204082,0.7142857142857142,0.7346938775510203,0.7551020408163265,0.7755102040816326,0.7959183673469387,0.8163265306122448,0.836734693877551,0.8571428571428571,0.8775510204081632,0.8979591836734693,0.9183673469387754,0.9387755102040816,0.9591836734693877,0.9795918367346939,1.0],"y":[0.0,0.02040816326530612,0.04081632653061224,0.061224489795918366,0.08163265306122448,0.1020408163265306,0.12244897959183673,0.14285714285714285,0.16326530612244897,0.18367346938775508,0.2040816326530612,0.22448979591836732,0.24489795918367346,0.26530612244897955,0.2857142857142857,0.3061224489795918,0.32653061224489793,0.3469387755102041,0.36734693877551017,0.3877551020408163,0.4081632653061224,0.42857142857142855,0.44897959183673464,0.4693877551020408,0.4897959183673469,0.5102040816326531,0.5306122448979591,0.5510204081632653,0.5714285714285714,0.5918367346938775,0.6122448979591836,0.6326530612244897,0.6530612244897959,0.673469387755102,0.6938775510204082,0.7142857142857142,0.7346938775510203,0.7551020408163265,0.7755102040816326,0.7959183673469387,0.8163265306122448,0.836734693877551,0.8571428571428571,0.8775510204081632,0.8979591836734693,0.9183673469387754,0.9387755102040816,0.9591836734693877,0.9795918367346939,1.0],"type":"scattergl","xaxis":"x2","yaxis":"y2"}],                        {"template":{"data":{"barpolar":[{"marker":{"line":{"color":"white","width":0.5},"pattern":{"fillmode":"overlay","size":10,"solidity":0.2}},"type":"barpolar"}],"bar":[{"error_x":{"color":"rgb(36,36,36)"},"error_y":{"color":"rgb(36,36,36)"},"marker":{"line":{"color":"white","width":0.5},"pattern":{"fillmode":"overlay","size":10,"solidity":0.2}},"type":"bar"}],"carpet":[{"aaxis":{"endlinecolor":"rgb(36,36,36)","gridcolor":"white","linecolor":"white","minorgridcolor":"white","startlinecolor":"rgb(36,36,36)"},"baxis":{"endlinecolor":"rgb(36,36,36)","gridcolor":"white","linecolor":"white","minorgridcolor":"white","startlinecolor":"rgb(36,36,36)"},"type":"carpet"}],"choropleth":[{"colorbar":{"outlinewidth":1,"tickcolor":"rgb(36,36,36)","ticks":"outside"},"type":"choropleth"}],"contourcarpet":[{"colorbar":{"outlinewidth":1,"tickcolor":"rgb(36,36,36)","ticks":"outside"},"type":"contourcarpet"}],"contour":[{"colorbar":{"outlinewidth":1,"tickcolor":"rgb(36,36,36)","ticks":"outside"},"colorscale":[[0.0,"#440154"],[0.1111111111111111,"#482878"],[0.2222222222222222,"#3e4989"],[0.3333333333333333,"#31688e"],[0.4444444444444444,"#26828e"],[0.5555555555555556,"#1f9e89"],[0.6666666666666666,"#35b779"],[0.7777777777777778,"#6ece58"],[0.8888888888888888,"#b5de2b"],[1.0,"#fde725"]],"type":"contour"}],"heatmapgl":[{"colorbar":{"outlinewidth":1,"tickcolor":"rgb(36,36,36)","ticks":"outside"},"colorscale":[[0.0,"#440154"],[0.1111111111111111,"#482878"],[0.2222222222222222,"#3e4989"],[0.3333333333333333,"#31688e"],[0.4444444444444444,"#26828e"],[0.5555555555555556,"#1f9e89"],[0.6666666666666666,"#35b779"],[0.7777777777777778,"#6ece58"],[0.8888888888888888,"#b5de2b"],[1.0,"#fde725"]],"type":"heatmapgl"}],"heatmap":[{"colorbar":{"outlinewidth":1,"tickcolor":"rgb(36,36,36)","ticks":"outside"},"colorscale":[[0.0,"#440154"],[0.1111111111111111,"#482878"],[0.2222222222222222,"#3e4989"],[0.3333333333333333,"#31688e"],[0.4444444444444444,"#26828e"],[0.5555555555555556,"#1f9e89"],[0.6666666666666666,"#35b779"],[0.7777777777777778,"#6ece58"],[0.8888888888888888,"#b5de2b"],[1.0,"#fde725"]],"type":"heatmap"}],"histogram2dcontour":[{"colorbar":{"outlinewidth":1,"tickcolor":"rgb(36,36,36)","ticks":"outside"},"colorscale":[[0.0,"#440154"],[0.1111111111111111,"#482878"],[0.2222222222222222,"#3e4989"],[0.3333333333333333,"#31688e"],[0.4444444444444444,"#26828e"],[0.5555555555555556,"#1f9e89"],[0.6666666666666666,"#35b779"],[0.7777777777777778,"#6ece58"],[0.8888888888888888,"#b5de2b"],[1.0,"#fde725"]],"type":"histogram2dcontour"}],"histogram2d":[{"colorbar":{"outlinewidth":1,"tickcolor":"rgb(36,36,36)","ticks":"outside"},"colorscale":[[0.0,"#440154"],[0.1111111111111111,"#482878"],[0.2222222222222222,"#3e4989"],[0.3333333333333333,"#31688e"],[0.4444444444444444,"#26828e"],[0.5555555555555556,"#1f9e89"],[0.6666666666666666,"#35b779"],[0.7777777777777778,"#6ece58"],[0.8888888888888888,"#b5de2b"],[1.0,"#fde725"]],"type":"histogram2d"}],"histogram":[{"marker":{"line":{"color":"white","width":0.6}},"type":"histogram"}],"mesh3d":[{"colorbar":{"outlinewidth":1,"tickcolor":"rgb(36,36,36)","ticks":"outside"},"type":"mesh3d"}],"parcoords":[{"line":{"colorbar":{"outlinewidth":1,"tickcolor":"rgb(36,36,36)","ticks":"outside"}},"type":"parcoords"}],"pie":[{"automargin":true,"type":"pie"}],"scatter3d":[{"line":{"colorbar":{"outlinewidth":1,"tickcolor":"rgb(36,36,36)","ticks":"outside"}},"marker":{"colorbar":{"outlinewidth":1,"tickcolor":"rgb(36,36,36)","ticks":"outside"}},"type":"scatter3d"}],"scattercarpet":[{"marker":{"colorbar":{"outlinewidth":1,"tickcolor":"rgb(36,36,36)","ticks":"outside"}},"type":"scattercarpet"}],"scattergeo":[{"marker":{"colorbar":{"outlinewidth":1,"tickcolor":"rgb(36,36,36)","ticks":"outside"}},"type":"scattergeo"}],"scattergl":[{"marker":{"colorbar":{"outlinewidth":1,"tickcolor":"rgb(36,36,36)","ticks":"outside"}},"type":"scattergl"}],"scattermapbox":[{"marker":{"colorbar":{"outlinewidth":1,"tickcolor":"rgb(36,36,36)","ticks":"outside"}},"type":"scattermapbox"}],"scatterpolargl":[{"marker":{"colorbar":{"outlinewidth":1,"tickcolor":"rgb(36,36,36)","ticks":"outside"}},"type":"scatterpolargl"}],"scatterpolar":[{"marker":{"colorbar":{"outlinewidth":1,"tickcolor":"rgb(36,36,36)","ticks":"outside"}},"type":"scatterpolar"}],"scatter":[{"fillpattern":{"fillmode":"overlay","size":10,"solidity":0.2},"type":"scatter"}],"scatterternary":[{"marker":{"colorbar":{"outlinewidth":1,"tickcolor":"rgb(36,36,36)","ticks":"outside"}},"type":"scatterternary"}],"surface":[{"colorbar":{"outlinewidth":1,"tickcolor":"rgb(36,36,36)","ticks":"outside"},"colorscale":[[0.0,"#440154"],[0.1111111111111111,"#482878"],[0.2222222222222222,"#3e4989"],[0.3333333333333333,"#31688e"],[0.4444444444444444,"#26828e"],[0.5555555555555556,"#1f9e89"],[0.6666666666666666,"#35b779"],[0.7777777777777778,"#6ece58"],[0.8888888888888888,"#b5de2b"],[1.0,"#fde725"]],"type":"surface"}],"table":[{"cells":{"fill":{"color":"rgb(237,237,237)"},"line":{"color":"white"}},"header":{"fill":{"color":"rgb(217,217,217)"},"line":{"color":"white"}},"type":"table"}]},"layout":{"annotationdefaults":{"arrowhead":0,"arrowwidth":1},"autotypenumbers":"strict","coloraxis":{"colorbar":{"outlinewidth":1,"tickcolor":"rgb(36,36,36)","ticks":"outside"}},"colorscale":{"diverging":[[0.0,"rgb(103,0,31)"],[0.1,"rgb(178,24,43)"],[0.2,"rgb(214,96,77)"],[0.3,"rgb(244,165,130)"],[0.4,"rgb(253,219,199)"],[0.5,"rgb(247,247,247)"],[0.6,"rgb(209,229,240)"],[0.7,"rgb(146,197,222)"],[0.8,"rgb(67,147,195)"],[0.9,"rgb(33,102,172)"],[1.0,"rgb(5,48,97)"]],"sequential":[[0.0,"#440154"],[0.1111111111111111,"#482878"],[0.2222222222222222,"#3e4989"],[0.3333333333333333,"#31688e"],[0.4444444444444444,"#26828e"],[0.5555555555555556,"#1f9e89"],[0.6666666666666666,"#35b779"],[0.7777777777777778,"#6ece58"],[0.8888888888888888,"#b5de2b"],[1.0,"#fde725"]],"sequentialminus":[[0.0,"#440154"],[0.1111111111111111,"#482878"],[0.2222222222222222,"#3e4989"],[0.3333333333333333,"#31688e"],[0.4444444444444444,"#26828e"],[0.5555555555555556,"#1f9e89"],[0.6666666666666666,"#35b779"],[0.7777777777777778,"#6ece58"],[0.8888888888888888,"#b5de2b"],[1.0,"#fde725"]]},"colorway":["#1F77B4","#FF7F0E","#2CA02C","#D62728","#9467BD","#8C564B","#E377C2","#7F7F7F","#BCBD22","#17BECF"],"font":{"color":"rgb(36,36,36)"},"geo":{"bgcolor":"white","lakecolor":"white","landcolor":"white","showlakes":true,"showland":true,"subunitcolor":"white"},"hoverlabel":{"align":"left"},"hovermode":"closest","mapbox":{"style":"light"},"paper_bgcolor":"white","plot_bgcolor":"white","polar":{"angularaxis":{"gridcolor":"rgb(232,232,232)","linecolor":"rgb(36,36,36)","showgrid":false,"showline":true,"ticks":"outside"},"bgcolor":"white","radialaxis":{"gridcolor":"rgb(232,232,232)","linecolor":"rgb(36,36,36)","showgrid":false,"showline":true,"ticks":"outside"}},"scene":{"xaxis":{"backgroundcolor":"white","gridcolor":"rgb(232,232,232)","gridwidth":2,"linecolor":"rgb(36,36,36)","showbackground":true,"showgrid":false,"showline":true,"ticks":"outside","zeroline":false,"zerolinecolor":"rgb(36,36,36)"},"yaxis":{"backgroundcolor":"white","gridcolor":"rgb(232,232,232)","gridwidth":2,"linecolor":"rgb(36,36,36)","showbackground":true,"showgrid":false,"showline":true,"ticks":"outside","zeroline":false,"zerolinecolor":"rgb(36,36,36)"},"zaxis":{"backgroundcolor":"white","gridcolor":"rgb(232,232,232)","gridwidth":2,"linecolor":"rgb(36,36,36)","showbackground":true,"showgrid":false,"showline":true,"ticks":"outside","zeroline":false,"zerolinecolor":"rgb(36,36,36)"}},"shapedefaults":{"fillcolor":"black","line":{"width":0},"opacity":0.3},"ternary":{"aaxis":{"gridcolor":"rgb(232,232,232)","linecolor":"rgb(36,36,36)","showgrid":false,"showline":true,"ticks":"outside"},"baxis":{"gridcolor":"rgb(232,232,232)","linecolor":"rgb(36,36,36)","showgrid":false,"showline":true,"ticks":"outside"},"bgcolor":"white","caxis":{"gridcolor":"rgb(232,232,232)","linecolor":"rgb(36,36,36)","showgrid":false,"showline":true,"ticks":"outside"}},"title":{"x":0.05},"xaxis":{"automargin":true,"gridcolor":"rgb(232,232,232)","linecolor":"rgb(36,36,36)","showgrid":false,"showline":true,"ticks":"outside","title":{"standoff":15},"zeroline":false,"zerolinecolor":"rgb(36,36,36)"},"yaxis":{"automargin":true,"gridcolor":"rgb(232,232,232)","linecolor":"rgb(36,36,36)","showgrid":false,"showline":true,"ticks":"outside","title":{"standoff":15},"zeroline":false,"zerolinecolor":"rgb(36,36,36)"}}},"xaxis":{"anchor":"y","domain":[0.0,0.45],"tickmode":"array","tickvals":[0,20,40,60,80,100],"ticktext":["0%","20%","40%","60%","80%","100%"],"title":{"text":"Predicted Risk"}},"yaxis":{"anchor":"x","domain":[0.0,0.6649999999999999],"tickmode":"array","tickvals":[0,20,40,60,80,100],"ticktext":["0%","20%","40%","60%","80%","100%"],"title":{"text":"Observed Risk"}},"xaxis2":{"anchor":"y2","domain":[0.55,1.0],"range":[-0.05,1],"tickmode":"array","tickvals":[0.0,0.2,0.4,0.6000000000000001,0.8,1.0],"title":{"text":"False Positive Rate"}},"yaxis2":{"anchor":"x2","domain":[0.0,0.6649999999999999],"tickmode":"array","tickvals":[0.0,0.2,0.4,0.6000000000000001,0.8,1.0],"title":{"text":"True Positive Rate"}},"annotations":[{"font":{"size":16},"showarrow":false,"text":"Predicted Risk","x":0.5,"xanchor":"center","xref":"paper","y":1.0,"yanchor":"bottom","yref":"paper"},{"font":{"size":16},"showarrow":false,"text":"Calibration","x":0.225,"xanchor":"center","xref":"paper","y":0.6649999999999999,"yanchor":"bottom","yref":"paper"},{"font":{"size":16},"showarrow":false,"text":"ROC Curve","x":0.775,"xanchor":"center","xref":"paper","y":0.6649999999999999,"yanchor":"bottom","yref":"paper"}],"autosize":false,"width":800,"height":600,"showlegend":false},                        {"responsive": true}                    )                };                            </script>        </div>
      </div>
  </body>
  </html>

  <script>
      var variable_names = ["(Intercept)","ClumpThickness","MarginalAdhesion","BareNuclei","BlandChromatin","Mitoses",];
      var rho = [-17,1,1,1,1,1,];
      var min_values = [1,1,1,1,1,1,];
      var max_values = [1,10,10,10,10,10,];
      var _min_values = [];
      var _max_values = [];
      var _rho_str = [];
      var _names = [];
      for (i=1; i<rho.length; i++){
          if (rho[i] > 0){
              sign = "+";
          } else {
              sign = "";
          }
          if (rho[i] > 1 || rho[i] < -1){
              pt = " points"
          } else {
              pt = " point"
          }
          _rho_str.push("" + sign + rho[i] + pt);
          _max_values.push(max_values[i]);
          _min_values.push(min_values[i]);
          _names.push(variable_names[i]);
      }
      var n_rows = rho.length-1;
      var table = document.createElement("TABLE");
      var dot = (a, b) => a.map((x, i) => a[i] * b[i]).reduce((m, n) => m + n);
      for(var i=0; i<n_rows; i++) {
          var row = table.insertRow(i);
          r0 = row.insertCell(0);
          r0.innerHTML = i+1 + ". ";
          r0.innerHTML += _names[i];
          row.insertCell(1).innerHTML = _rho_str[i];
          // Define input field
          var val_input = document.createElement("input");
          val_input.type = "number";
          val_input.defaultValue = _min_values[i];
          val_input.id = "input_" + i;
          val_input.min = _min_values[i];
          val_input.max = _max_values[i];
          val_input.style.width = "70px";
          val_input.class = "quantity";
          // Insert input into div
          var div = document.createElement("div");
          div.className = "quantity";
          div.innerHTML += "×    ";
          div.append(val_input);
          div.innerHTML += " + ..."
          // Insert input into table
          r = row.insertCell(2)
          //r.innerHTML += "× ";
          r.appendChild(div);
          //r.innerHTML += " + ...";
          if (i == n_rows-1){
              // Score
              var row_score = table.insertRow(i+1);
              row_score0 = row_score.insertCell(0);
              row_score0.innerHTML = "";
              row_score1 = row_score.insertCell(1);
              row_score1.innerHTML = "SCORE";
              row_score2 = row_score.insertCell(2);
              row_score2.innerHTML = "" + min_values.slice(1).reduce((a, b) => a + b, 0);
              // Risk
              var row_risk = table.insertRow(i+2);
              row_risk0 = row_risk.insertCell(0);
              row_risk0.innerHTML = "";
              row_risk1 = row_risk.insertCell(1);
              row_risk1.innerHTML = "RISK";
              row_risk2 = row_risk.insertCell(2);
              row_risk2.innerHTML = "" + (100 / (1+Math.exp(-dot(min_values, rho)))).toFixed(3) + "%";
          }
      }
      document.getElementById("main_div").prepend(table);
      // Jquery to update table
      var parse_input = function(n_rows) {
          $(':input').change(function () {
              var scores = [1];
              var score = 0;
              for (i=0; i<n_rows; i++) {
                  value = $("#input_" + i);
                  value = value.val();
                  // Enfore min/max constraint
                  if (value > _max_values[i]){
                      value = _max_values[i]
                      $("#input_" + i).val(value)
                  } else if (value < _min_values[i]){
                      value = _min_values[i]
                      $("#input_" + i).val(value)
                  }
                  score += parseInt(value);
                  scores.push(value);
              }
              row_score2.innerHTML = "" + score;
              row_risk2.innerHTML = "" + (100 / (1+Math.exp(-dot(scores, rho)))).toFixed(3) + "%";
              console.log(score);
          });
      };
      parse_input(n_rows);
      // Custom increment buttons
      $(document).ready(function () {
      jQuery('<div class="quantity-nav"><button class="quantity-button quantity-up">&#xf106;</button><button class="quantity-button quantity-down">&#xf107</button></div>').insertAfter('.quantity input');
      jQuery('.quantity').each(function () {
          var spinner = jQuery(this),
              input = spinner.find('input[type="number"]'),
              btnUp = spinner.find('.quantity-up'),
              btnDown = spinner.find('.quantity-down'),
              min = input.attr('min'),
              max = input.attr('max');

          btnUp.click(function () {
          var oldValue = parseFloat(input.val());
          if (oldValue >= max) {
              var newVal = oldValue;
          } else {
              var newVal = oldValue + 1;
          }
          spinner.find("input").val(newVal);
          spinner.find("input").trigger("change");
          });

          btnDown.click(function () {
          var oldValue = parseFloat(input.val());
          if (oldValue <= min) {
              var newVal = oldValue;
          } else {
              var newVal = oldValue - 1;
          }
          spinner.find("input").val(newVal);
          spinner.find("input").trigger("change");
          });

      });
      });
  </script>
  <style>
      table {
          table-layout: fixed;
          font-family: "Open Sans", verdana, arial, sans-serif;
          border-collapse: collapse;
          width: 800px;
          background-color: rgb(237, 237, 237);
      }
      td:hover {background-color: rgb(218, 218, 218);}
      td, th {
          text-align: left;
          padding: 5px;
      }
      tr:nth-child(1) {
          border-top: solid 2px black;
      }
      td:nth-child(1) {
          border-left: solid 2px black;
      }
      td:nth-child(3){
          border-right: solid 2px black;
      }
      tr:nth-last-child(3) {
          border-bottom: solid 2px black;
      }
      td:nth-last-child(1) {
          border-left: solid 2px black;
      }
      tr:last-child {
          border-bottom: solid 2px black;
      }
      h3{
          font-family: "Open Sans", verdana, arial, sans-serif;
      }
      #main_div, #report_header {
          display: block;
          margin-left: auto;
          margin-right: auto;
          width: 50%;
      }
      /* Style buttons */
      /* .quantity {
          position: relative;
      } */
      input[type=number]::-webkit-inner-spin-button,
      input[type=number]::-webkit-outer-spin-button {
          -webkit-appearance: none;
          margin: 0;
      }
      input[type=number] {
          -moz-appearance: textfield;
      }
      .quantity input {
          width: 37px;
          height: 28px;
          /* line-height: 1.65; */
          /* float: inline-start; */
          /* display: block; */
          /* padding: 0;
          margin: 0; */
          padding-left: 20px;
          border: none;
          box-shadow: 0 0 0 1px rgba(0, 0, 0, 0.08);
          font-size: 1rem;
          border-radius: 2px;
      }
      /* .quantity input:focus {
          outline: 0;
      } */
      .quantity-nav {
          float: right;
          position: relative;
          height: 28px;
          right: 65%;
      }
      .quantity-button {
          position: relative;
          cursor: pointer;
          border: none;
          border-left: 1px solid rgba(0, 0, 0, 0.08);
          width: 21px;
          text-align: center;
          color: #333;
          font-size: 13px;
          font-family: "FontAwesome" !important;
          /* line-height: 1;
          padding: 0; */
          background: #FAFAFA;
          -webkit-transform: translateX(-100%);
          transform: translateX(-100%);
          -webkit-user-select: none;
          -moz-user-select: none;
          -ms-user-select: none;
          -o-user-select: none;
          user-select: none;
      }
      .quantity-button:active {
          background: #EAEAEA;
      }
      .quantity-button.quantity-up {
          position: absolute;
          height: 50%;
          top: 0;
          border-bottom: 1px solid rgba(0, 0, 0, 0.08);
          font-family: "FontAwesome";
          border-radius: 0 4px 0 0;
      }
      .quantity-button.quantity-down {
          position: absolute;
          bottom: 0;
          height: 50%;
          font-family: "FontAwesome";
          border-radius: 0 0 4px 0;
      }
  </style>


Contributing
------------

I'm planning to pick up development again in Fall 2020. I can definitely use a hand! If you are interested in contributing, please reach out!

Here's the current development roadmap:

- `sci-kit learn interface <http://scikit-learn.org/stable/developers/contributing.html#rolling-your-own-estimator>`_
- support for open source solver in `python-mip <https://github.com/coin-or/python-mip>`_
- basic reporting tools (roc curves, calibration plots, model reports)
- documentation
- pip

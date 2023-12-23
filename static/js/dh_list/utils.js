function ajaxCall(url, method, data, successCallback, errorCallback) {
    $.ajax({
        url: url,
        method: method,
        data: data,
        success: function(response) {
            if (successCallback) {
                successCallback(response);
            }
        },
        error: function(xhr, status, error) {
            if (errorCallback) {
                errorCallback(xhr, status, error);
            }
        }
    });
}

function createOrShowModal(body) {
    // 检查页面上是否存在模态框
    var myModal = document.getElementById('dynamicModal');
    if (!myModal) {
        // 创建模态框的HTML
        var modalHtml = `
            <div class="modal fade" id="dynamicModal" tabindex="-1" aria-labelledby="dynamicModalLabel" aria-hidden="true" style="display: none;">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="dynamicModalLabel">提示</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body"></div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-primary" onclick="window.location.replace(document.referrer)">返回</button>
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">关闭</button>
                        </div>
                    </div>
                </div>
            </div>
        `;

        // 将模态框的HTML添加到页面
        document.body.insertAdjacentHTML('beforeend', modalHtml);
    }

    // 获取模态框元素并修改内容
    myModal = document.getElementById('dynamicModal');
    document.querySelector('.modal-body').innerHTML = body;

    // 创建并显示模态框
    var modal = new bootstrap.Modal(myModal);
    modal.show();
}

// 复制到剪贴板
copyInnerTextOfCell = (event) => {
    let innerText = event.target.innerText;
    var tmpInput = document.createElement("input");
    document.body.appendChild(tmpInput);
    tmpInput.value = innerText;
    tmpInput.select();
    document.execCommand("cut"); // copy
    tmpInput.remove();
    showMsg("复制成功：" + innerText);
  }
//显示框信息
function showMsg(val,time){
   if(!document.getElementById('parent_pop_up')){
      var parent_pop_up = document.createElement('div');
      parent_pop_up.id = "parent_pop_up";
      parent_pop_up.style.cssText = "position: fixed; z-index: 9999; bottom: 5rem; width: 100%;";
      var poo_up = document.createElement('div');
      poo_up.id = 'poo_up';
      poo_up.style.cssText = 'height: 1rem; margin:0 auto; text-align: center;';
      var span = document.createElement('span');
      span.style.cssText = 'background-color: rgba(0,0,0,0.6); padding: 0.2rem 0.35rem; letter-spacing: 3px; border-radius: 10px; color: #FFFFFF; font-size: 2.8rem; text-align: center;';
      span.innerHTML = val;
      poo_up.appendChild(span);
      parent_pop_up.appendChild(poo_up);
      document.body.appendChild(parent_pop_up);
      if(time == null || time == ''){
         time = 1500;
      }
      setTimeout(function(){hideMsg();},time);
   }
}
//隐藏显示框
function hideMsg(){
   var pop = document.getElementById('parent_pop_up');
   pop.style.display = 'none';
   document.body.removeChild(pop);
}
    function httpget(url){
        var httpRequest = new XMLHttpRequest();
        httpRequest.open('GET', url, true);
        httpRequest.send();
        location.reload()
    }

function updateguard() {
    ajaxCall('/dhlist/api/upguards','GET',null, function (response) {
                if (response.code === 200) {
                    createOrShowModal('更新成功！');
                } else {
                    createOrShowModal('更新失败！');
                }
            },
            function (error) {
                createOrShowModal('连接错误！');
            });
}
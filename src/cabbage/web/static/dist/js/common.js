/**
function chanageCondition(type,names){	
	var c= "#conditionId";
	$(c).attr("name",names[type]);
}
$(function(){
	$("#condition").blur(function(){
		  $("#conditionId").val(this.value);
	});
});*/

function setMenuActive(dataKey)
{
	var li = $("[data-key='"+dataKey+"']")
	var ul = $(li).parent()
	var a = $(li).children("a")
	
	$(a).addClass('active')
	
	$(ul).collapse("toggle");
	
	$(ul).parent("li").addClass('active')
	
	
//	console.log(ul)
//	console.log(a)
}


function submitQuery(formId){
	var c= "#"+formId;
	$(c).submit();
}
function submitTabQuery(formId,typeId,typeValue){
	var form = "#"+formId;
	var type = "#"+typeId;
	$(type).val(typeValue);
	cleanPage();
	$(form).submit();
}
function ajax(url,params,success,error){
			$.ajax({
				url:url,
				data:params,
				timeout: 2000000,
				success: success,
			    error: error
			});
}
function ajaxAsync(url,params,async,success,error){
			$.ajax({
				url:url,
				type:'POST',
				data:params,
				async:async,
				dataType:'json',
				timeout: 2000000,
				success: success,
			    error: error
			});
}
function initAutoQuery(key,url,callback){
	
	$('#'+key).autocomplete({
			    serviceUrl:''+url,
			    paramName:'key',
			    type:'post',
			    onSelect:function(suggestion){ callback(suggestion);}
	});
}

function formValidate(form,errorTip, moreOption){
	var basicOption = {
			invalidHandler: function(event, validator) {
			    // 'this' refers to the form
			    var errors = validator.numberOfInvalids();
			    if (errors) {
			      $("#"+errorTip).show();
			    } else {
			      $("#"+errorTip).hide();
			    }
			  },
			showErrors:function(errorMap,errorList) {
		    			if(errorList && errorList.length >0){
		    				var firstElement = errorList[0];
		    				 $("#"+errorTip).html(firstElement.message);
		    				// console.log(firstElement);
		    				 //firstElement.element.focus();
		    			}
			  }
		};
	
	if(moreOption)
	{
		basicOption = $.extend(basicOption, moreOption);
	}
	
	$("#"+form).validate(basicOption);
}

function isNumber(value){
	var z= /^[0-9]*$/;
	return z.test(value);
}




/**  
 * 数字格式转换成千分位  
 *@param{Object}num  
 */  
function commafy(num) {   
	//1.先去除空格,判断是否空值和非数   
	num = num + "";   
	num = num.replace(/[ ]/g, ""); //去除空格  
    if (num == "") {   
    return;   
    }   
    if (isNaN(num)){  
    return;   
    }   
    //2.针对是否有小数点，分情况处理   
    var index = num.indexOf(".");   
    if (index==-1) {//无小数点   
      var reg = /(-?\d+)(\d{3})/;   
        while (reg.test(num)) {   
        num = num.replace(reg, "$1,$2");   
        }   
    } else {   
        var intPart = num.substring(0, index);   
        var pointPart = num.substring(index + 1, num.length);   
        var reg = /(-?\d+)(\d{3})/;   
        while (reg.test(intPart)) {   
        intPart = intPart.replace(reg, "$1,$2");   
        }   
       num = intPart +"."+ pointPart;   
    }   
    return num;   
}

Array.prototype.contains = function(item){
    for(i=0;i<this.length;i++){
        if(this[i]==item){
	        return true;
	    }
    }
    return false;
};

Array.prototype.remove = function(item) {
	var n = -1;
	var l = this.length;
	for (var i = 0; i < l; i++) {
		if(this[i] == item){
			n = i;
			break;
		}
	}
	if(n == -1){
		return this;
	}
	return this.slice(0, n).concat(this.slice(n + 1, l));
};

$(function(){
	

});
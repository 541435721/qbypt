/**
 * Created by k on 2017/4/25.
 */
 var partClass = new Array()               //用来记录类型和部位选项的关系 是1对多的关系
        var partPrice = new Array()
        //部位价格
        function alter_part_price(part, price) {          //初始化部位。初始化partClass的数据 part 是
            partPrice[part] = price;           //初始化部位。初始化partClass的数据
        }

        function alter_choose_checkbox(part, classify) {          //初始化部位。初始化partClass的数据 part 是
            partClass[part] = classify;           //初始化部位。初始化partClass的数据
            var sel = document.getElementById('id_classify');           //获取类型框对象
            var selected_val = sel.options[sel.selectedIndex].value;       //获取类型框所选内容
            if (classify != selected_val)                  //判断是不是属于选择的该类
                document.getElementById('id_part_' + String(parseInt(part) - 1)).parentNode.parentNode.style.display = "none"; //如果不是 那么隐藏
            else
                document.getElementById('id_part_' + String(parseInt(part) - 1)).parentNode.parentNode.style.display = "";     //如果是 显示
        }

        function alter_chooseParts(selected_parts) {
            document.getElementById('id_part_' + String(parseInt(selected_parts) - 1)).checked = true
            document.getElementById('id_part_' + String(parseInt(selected_parts) - 1)).onclick = function () {
                return false;
            }
        }

        function alter_change_checkbox() {                 //重新选择类的时候 调整新的选择部位
            var sel = document.getElementById('id_classify');
            var selected_val = sel.options[sel.selectedIndex].value;
            var price = document.getElementById('price')
            for (var i = 1; i <= partClass.length; i++)      // 遍历所有的部位
            {
                if (partClass[i] == selected_val)          // 如果该部位对应的类型是选择的类型
                    document.getElementById('id_part_' + String(i - 1)).parentNode.parentNode.style.display = ""; //显示出来 'id_part_'+String(i-1) 是获取到对应的li
                else {
                    if (document.getElementById('id_part_' + String(i - 1)).checked) {           // 如果不是该类型的话 看该部位之前是不是被选中
                        document.getElementById('id_part_' + String(i - 1)).checked = false;    // 变成未选中
                        price.innerHTML = parseInt(price.innerHTML) - partPrice[i]              //减掉价格
                    }
                    document.getElementById('id_part_' + String(i - 1)).parentNode.parentNode.style.display = "none";       // 隐藏该部位
                }
            }
        }

        var partRelation = new Array()
        var partRelation = new Array(); //先声明一维

        for (var i = 0; i < 50; i++) {  //一维长度为2
            partRelation[i] = new Array(); //再声明二维
            for (var j = 0; j < 50; j++) {  //二维长度为3
                partRelation[i][j] = 0;  // 赋值，每个数组元素的值为i+j
            }
        }

        function alter_checkbox_relation(part_son, part_father) {
            partRelation[part_son][part_father] = 1;
        }

        function alter_get_relation_checkbox(part) {
            var changed_checkbox = document.getElementById('id_part_' + String(parseInt(part) - 1))
            var son_checkbox
            var price = document.getElementById('price')
            if (changed_checkbox.checked) {
                price.innerHTML = parseInt(price.innerHTML) + partPrice[part]
                for (var i = 1; i <= partClass.length; i++) {
                    if (partRelation[i][part] == 1) {
                        son_checkbox = document.getElementById('id_part_' + String(i - 1))
                        if (!son_checkbox.checked) {
                            son_checkbox.checked = true
                            price.innerHTML = parseInt(price.innerHTML) + partPrice[i]
                        }
                    }
                }
            }
            else {
                price.innerHTML = parseInt(price.innerHTML) - partPrice[part]
                for (var i = 1; i <= partClass.length; i++) {
                    if (partRelation[part][i] == 1) {
                        son_checkbox = document.getElementById('id_part_' + String(i - 1))
                        if (son_checkbox.checked) {
                            son_checkbox.checked = false
                            price.innerHTML = parseInt(price.innerHTML) - partPrice[i]
                        }

                    }
                }
            }
        }
        function disable() {
            var osel = document.getElementById("id_classify");
            osel.onfocus = function () {
                this.defaultIndex = this.selectedIndex;
            }
            osel.onchange = function () {
                this.selectedIndex = this.defaultIndex;
            }
        }

        function customer_project_alter(project_id) {
            location.href = "/customer_project_alter/?project_id=" + project_id;
        }

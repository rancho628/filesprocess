webix.ready(function(){
  webix.ui({
    rows: [
      { view: "toolbar", padding:3, elements: [
        { view: "icon", icon: "mdi mdi-menu", click: function(){
           $$("$sidebar1").toggle();
         }
        },
        { view: "label", label: "My App"},
        {},
        { view: "icon", icon: "mdi mdi-comment",  badge:4},
        { view: "icon", icon: "mdi mdi-bell",  badge:10}
      ]
      },
      { cols:[
        {
          view: "sidebar",
          data: menu_data,
          on:{
            onAfterSelect: function(id){
              webix.message("Selected: "+this.getItem(id).value)
            }
          }
        },
        { template: ""}
      ]}
    ]
  });
});
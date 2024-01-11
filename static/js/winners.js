/* eslint-disable */
$(function () {
  var winnersGrid;

  var initializeWinnersGrid = function () {
    winnersGrid = $("#winners-grid")
      .kendoGrid({
        dataSource: {
          transport: {
            read: {
              url: site_url + "lottery/winners/all/",
              dataType: "json",
            },
          },
          pageSize: 15,
        },
        sortable: true,
        pageable: {
          refresh: true,
          pageSizes: true,
          buttonCount: 5,
        },
        columns: [
          {
            template:
              "<div class='customer-photo'></div>" +
              "<div class='customer-name'>#: name #</div>",
            field: "name",
            title: "中奖者",
          },
          {
            field: "chineseName",
            title: "中文名",
          },
          {
            field: "award",
            title: "奖项",
          },
          {
            field: "prize",
            title: "奖品",
          },
          {
            field: "is_valid",
            title: "是否生效",
          },
        ],
      })
      .data("kendoGrid");
  };

  initializeWinnersGrid();
});

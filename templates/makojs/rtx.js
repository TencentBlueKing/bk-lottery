var rtxs = [];
% for item in rtxs[:1000]:
    % if item.avatar is None:
        rtxs.push({name:'${item.name}', name_zh:'${item.chinese_name}', avatar:'${STATIC_URL}avatars/default.png'});
    % else:
        rtxs.push({name:'${item.name}', name_zh:'${item.chinese_name}',avatar:'${item.avatar}'});
    % endif
% endfor

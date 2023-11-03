odoo.define('booking_snippet.snippet', function(require) {
'use strict';
var PublicWidget = require('web.public.widget');
var rpc = require('web.rpc');
var core = require('web.core');
var qweb = core.qweb;
var Dynamic = PublicWidget.Widget.extend({

selector: '.dynamic_snippet_blog',

start: function() {
console.log('.....................')
var self = this;

rpc.query({

route: '/booking_details',

}).then(function(data) {
console.log('data', data)
var chunks = _.chunk(data, 4)
console.log('11111',chunks)
chunks[0].is_active = true
self.$('#courosel').html(qweb.render('travel_management.booking_carousel', {chunks}))
});
}
});
PublicWidget.registry.dynamic_snippet_blog = Dynamic;
return Dynamic;
});


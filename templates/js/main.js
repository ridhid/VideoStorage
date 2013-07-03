/**
 * Created with PyCharm.
 * User: ridhid
 * Date: 27.06.13
 * Time: 15:52
 * To change this template use File | Settings | File Templates.
 */
function AppViewModel(){
    var self = this;
    this.dir = ko.observable();
    this.back_path = ko.observable();
    this.page = ko.observable();
    this.cwd = ko.observable("root");
    this.video = ko.observable(false);
    this.previous_page = function() {
        if (self.page().previous) {
            var page = self.page();
            page.current = page.previous;
            self.page(page);
        }
    };
    this.next_page = function() {
        if (self.page().next) {
            var page = self.page();
            page.current = page.next;
            self.page(page);
        }
    };
    this.reset_page = function() {
        var page = self.page();
        page.current = 1;
        self.page(page);
    };
    this.click = function(link) {
        if (link.url == null)
            self.into(link);
        else {
            self.video(false);
            self.video(link.url);
        }
    };
    this.into = function(folder) {
        self.reset_page();
        var cwd = self.cwd() == "root"? "" : self.cwd();
        self.cwd(cwd + '|' + folder.name);
    };
    this.to_root = function() {
        self.reset_page();
        self.cwd("root");
    };
    this.back_to = function(folder) {
        if (folder != "root")
            self.cwd(self.cwd().replace(new RegExp('(.*'+folder+').*', 'g'), '$1'));
        else
            self.to_root();
    };
    this.location_hash = ko.computed(function() {
        console.log('yeeehhh!');
        var params = {
            cwd: self.cwd(),
            page: self.page()
        }
        if (params.page != null && params.cwd != null)
            location.hash = 'fs/' + params.cwd + '/' + params.page.current;
    }, this);
    Sammy(function() {
        this.get('#fs/:path/:page', function() {
            var path = this.params.path == "root" ? "" : this.params.path.replace(/\|/g, '/');
            $.get(url, {format: 'json', path: path, page: this.params.page}, function(data) {
                self.dir(data.dir);
                self.back_path(add_root(data.back_path));
                self.page(data.page);
            })
        });
    }).run('#fs/root/1');
}

function add_root(bp) {
    return bp.reverse(), bp.push('root'), bp.reverse(), bp;
}

$(document).ready(function() {
    Model = new AppViewModel();
    ko.applyBindings(Model);
});
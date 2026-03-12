window.gpc_inject_hide = function () {
<<<<<<< HEAD
    let pg = frappe.pages["permission-manager"];
    if (!pg) return;
    let engine = pg.permission_engine;
    if (!engine || !engine.perm_list || !engine.table) return;
    if (engine.get_doctype() !== "Salary Slip") return;

    (engine.perm_list || []).forEach((d) => {
        if (d.permlevel !== 0) return;

        let row = engine.table.find("tbody tr").filter(function () {
            return $(this).find("td[data-fieldname='role']").text().replace(/\s+/g, ' ').trim().startsWith(d.role);
        });
        if (!row.length) return;

        let pc = row.find("td[data-fieldname='permissions'] div.row");
        if (!pc.length || pc.find("div[data-fieldname='hide']").length) return;

        pc.append(`<div class='col-md-4' data-fieldname='hide'><div class='checkbox'><label style='text-transform:capitalize'><input type='checkbox' data-ptype='hide' data-role='${d.role}' data-permlevel='${d.permlevel}' data-doctype='${d.parent}' ${d.hide ? "checked" : ""}>Hide</label></div></div>`);
    });

    engine.body.off("click.hide_patch").on("click.hide_patch", "input[data-ptype='hide']", function () {
        frappe.dom.freeze();
        let chk = $(this);
        frappe.call({
            method: "salary_slip_control.overrides.permission_manager.update",
            args: {
                role: chk.attr("data-role"),
                permlevel: chk.attr("data-permlevel"),
                doctype: chk.attr("data-doctype"),
                ptype: "hide",
                value: chk.prop("checked") ? 1 : 0,
            },
            callback: (r) => {
                frappe.dom.unfreeze();
                if (r.exc) {
                    chk.prop("checked", !chk.prop("checked"));
                    frappe.msgprint(__("Failed to update Hide permission."));
                } else {
                    frappe.show_alert({ message: __("Hide permission updated."), indicator: "green" });
                }
            },
        });
    });
};

frappe.router.on("change", function () {
    if (frappe.get_route()[0] !== "permission-manager") return;
    let attempts = 0;
    let poll = setInterval(function () {
        attempts++;
        let engine = frappe.pages["permission-manager"] && frappe.pages["permission-manager"].permission_engine;
        if (!engine) {
            if (attempts > 30) clearInterval(poll);
            return;
        }
        clearInterval(poll);
        if (!engine.__hide_patched) {
            engine.__hide_patched = true;
            let orig = engine.render.bind(engine);
            engine.render = function (perm_list) {
                orig(perm_list);
                setTimeout(window.gpc_inject_hide, 0);
            };
        }
        window.gpc_inject_hide();
    }, 200);
});

$(document).on("page-change", function () {
    if (frappe.get_route()[0] === "permission-manager") {
        setTimeout(window.gpc_inject_hide, 800);
    }
=======
	let pg = frappe.pages["permission-manager"];
	if (!pg) return;
	let engine = pg.permission_engine;
	if (!engine || !engine.perm_list || !engine.table) return;

	let doctype = engine.get_doctype();
	if (doctype !== "Salary Slip") return;

	(engine.perm_list || []).forEach((d) => {
		if (d.permlevel !== 0) return;

		let row = engine.table.find("tbody tr").filter(function () {
			return $(this)
				.find("td[data-fieldname='role']")
				.text()
				.replace(/\s+/g, " ")
				.trim()
				.startsWith(d.role);
		});
		if (!row.length) return;

		let pc = row.find("td[data-fieldname='permissions'] div.row");
		if (!pc.length || pc.find("div[data-fieldname='hide']").length) return;

		pc.append(
			`<div class='col-md-4' data-fieldname='hide'><div class='checkbox'><label style='text-transform:capitalize'><input type='checkbox' data-ptype='hide' data-role='${d.role}' data-permlevel='${d.permlevel}' data-doctype='${d.parent}' ${d.hide ? "checked" : ""}>Hide</label></div></div>`,
		);
	});

	engine.body
		.off("click.hide_patch")
		.on("click.hide_patch", "input[data-ptype='hide']", function () {
			frappe.dom.freeze();
			let chk = $(this);
			frappe.call({
				method: "salary_slip_control.overrides.permission_manager.update",
				args: {
					role: chk.attr("data-role"),
					permlevel: chk.attr("data-permlevel"),
					doctype: chk.attr("data-doctype"),
					ptype: "hide",
					value: chk.prop("checked") ? 1 : 0,
				},
				callback: (r) => {
					frappe.dom.unfreeze();
					if (r.exc) {
						chk.prop("checked", !chk.prop("checked"));
						frappe.msgprint(__("Failed to update Hide permission."));
					} else {
						frappe.show_alert({
							message: __("Hide permission updated."),
							indicator: "green",
						});
					}
				},
			});
		});
};

frappe.router.on("change", function () {
	if (frappe.get_route()[0] !== "permission-manager") return;
	let attempts = 0;
	let poll = setInterval(function () {
		attempts++;
		let engine =
			frappe.pages["permission-manager"] &&
			frappe.pages["permission-manager"].permission_engine;
		if (!engine) {
			if (attempts > 30) clearInterval(poll);
			return;
		}
		clearInterval(poll);
		if (!engine.__hide_patched) {
			engine.__hide_patched = true;
			let orig = engine.render.bind(engine);
			engine.render = function (perm_list) {
				orig(perm_list);
				setTimeout(window.gpc_inject_hide, 0);
			};
		}
		window.gpc_inject_hide();
	}, 200);
});

$(document).on("page-change", function () {
	if (frappe.get_route()[0] === "permission-manager") {
		setTimeout(window.gpc_inject_hide, 800);
	}
>>>>>>> fb4a87768200339635bff7e5e2f939779cc64346
});

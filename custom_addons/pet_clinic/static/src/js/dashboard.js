/** @odoo-module */

import { registry } from "@web/core/registry";
import { Component, useState, onWillStart } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

const PER_PAGE = 6;

class PetClinicDashboard extends Component {
    static template = "pet_clinic.Dashboard";
    static props = ["*"];

    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.state = useState({
            // Filters
            lokasi_id: false,
            date_from: this._getFirstDayOfMonth(),
            date_to: this._getToday(),
            // KPI
            visitationCount: 0,
            memberCount: 0,
            petCount: 0,
            doctorCount: 0,
            // Service table
            serviceFilter: "month",
            serviceData: [],
            servicePage: 0,
            serviceTotal: 0,
            // Penanganan table
            penangananFilter: "month",
            penangananData: [],
            penangananPage: 0,
            penangananTotal: 0,
            // Kunjungan Hari Ini
            visitationsToday: [],
            visitationPage: 0,
            visitationTotal: 0,
            // Janji Hari Ini
            appointmentsToday: [],
            appointmentPage: 0,
            appointmentTotal: 0,
            // Notif
            notifData: [],
            // Locations
            locations: [],
            // Search and Filters
            searchService: "",
            filterServiceType: "",
            searchPenanganan: "",
            filterPenangananStatus: "",
            searchVisitation: "",
            searchAppointment: "",
            serviceTypes: [],
            // Product Management
            productData: [],
            productPage: 0,
            productTotal: 0,
            searchProduct: "",
            filterProductType: "",
            productPeriod: "month",
            productSummary: {
                totalActive: 0,
                lowStockCount: 0,
                topProduct: "-",
                topProductCount: 0,
            },
        });

        onWillStart(async () => {
            await this._fetchLocations();
            await this._fetchServiceTypes();
            await this._fetchDashboardData();
        });
    }

    _getToday() {
        const d = new Date();
        return d.toISOString().split("T")[0];
    }

    _getFirstDayOfMonth() {
        const d = new Date();
        d.setDate(1);
        return d.toISOString().split("T")[0];
    }

    async _fetchLocations() {
        const locations = await this.orm.searchRead("pet_clinic.lokasi", [], ["id", "name"]);
        this.state.locations = locations;
    }

    async _fetchServiceTypes() {
        const types = await this.orm.searchRead("product.product", [["type", "=", "service"]], ["id", "name"]);
        this.state.serviceTypes = types;
    }

    async _fetchDashboardData() {
        const visitationDomain = [];
        const appointmentDomain = [];
        const doctorDomain = [["active", "=", true]];
        const memberDomain = [["active", "=", true]];
        const petDomain = [["active", "=", true]];

        if (this.state.lokasi_id) {
            const lokasiId = parseInt(this.state.lokasi_id);
            visitationDomain.push(["lokasi_pemeriksaan", "=", lokasiId]);
            appointmentDomain.push(["location_id", "=", lokasiId]);
            doctorDomain.push(["lokasi_ids", "in", [lokasiId]]);
            memberDomain.push(["pet_ids.visitation_ids.lokasi_pemeriksaan", "=", lokasiId]);
            petDomain.push(["visitation_ids.lokasi_pemeriksaan", "=", lokasiId]);
        }
        if (this.state.date_from) {
            visitationDomain.push(["date_start", ">=", this.state.date_from + " 00:00:00"]);
            appointmentDomain.push(["date", ">=", this.state.date_from + " 00:00:00"]);
        }
        if (this.state.date_to) {
            visitationDomain.push(["date_start", "<=", this.state.date_to + " 23:59:59"]);
            appointmentDomain.push(["date", "<=", this.state.date_to + " 23:59:59"]);
        }

        this.state.visitationCount = await this.orm.searchCount("pet_clinic.visitation", visitationDomain);
        this.state.memberCount = await this.orm.searchCount("pet_clinic.client", memberDomain);
        this.state.petCount = await this.orm.searchCount("pet_clinic.pet", petDomain);
        this.state.doctorCount = await this.orm.searchCount("pet_clinic.doctor", doctorDomain);

        // Reset pages on filter change
        this.state.servicePage = 0;
        this.state.penangananPage = 0;
        this.state.visitationPage = 0;
        this.state.appointmentPage = 0;

        // Refresh service types dropdown sinkron dengan lokasi aktif
        await this._fetchServiceTypes();

        await this._fetchServiceData();
        await this._fetchPenangananData();
        await this._fetchTodayVisitations();
        await this._fetchTodayAppointments();
        await this._fetchProductData();
        await this._fetchNotifData();
    }

    // ─── Service ──────────────────────────────────────────────────────────────
    _getServiceDomain() {
        const domain = this._getDateDomainForField(this.state.serviceFilter, "date_handling");
        if (this.state.lokasi_id) {
            domain.push(["visitation_lokasi_id", "=", parseInt(this.state.lokasi_id)]);
        }
        if (this.state.searchService) {
            domain.push("|", "|", "|", ["name", "ilike", this.state.searchService], ["nama_pemilik.name", "ilike", this.state.searchService], ["pet_id.name", "ilike", this.state.searchService], ["penanggung_jawab_name", "ilike", this.state.searchService]);
        }
        if (this.state.filterServiceType) {
            domain.push(["service_type", "=", parseInt(this.state.filterServiceType)]);
        }
        return domain;
    }

    onSearchService(ev) {
        this.state.searchService = ev.target.value;
        if (this.searchServiceTimeout) clearTimeout(this.searchServiceTimeout);
        this.searchServiceTimeout = setTimeout(() => {
            this.state.servicePage = 0;
            this._fetchServiceData();
        }, 300);
    }

    async onFilterServiceType(ev) {
        this.state.filterServiceType = ev.target.value;
        this.state.servicePage = 0;
        await this._fetchServiceData();
    }

    async _fetchServiceData() {
        const domain = this._getServiceDomain();
        this.state.serviceTotal = await this.orm.searchCount("pet_clinic.service", domain);
        const services = await this.orm.searchRead(
            "pet_clinic.service",
            domain,
            ["name", "service_type", "nama_pemilik", "pet_id", "penanggung_jawab_name", "visitation_lokasi_id", "date_handling", "visitation_id"],
            { limit: PER_PAGE, offset: this.state.servicePage * PER_PAGE, order: "date_handling desc" }
        );
        this.state.serviceData = services;
    }

    async serviceNext() {
        this.state.servicePage++;
        await this._fetchServiceData();
    }

    async servicePrev() {
        if (this.state.servicePage > 0) {
            this.state.servicePage--;
            await this._fetchServiceData();
        }
    }

    showAllService() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Semua Layanan",
            res_model: "pet_clinic.service",
            view_mode: "list,form",
            views: [[false, "list"], [false, "form"]],
            domain: this._getServiceDomain(),
            context: {},
        });
    }

    // ─── Penanganan ───────────────────────────────────────────────────────────
    _getPenangananDomain() {
        const domain = this._getDateDomainForField(this.state.penangananFilter, "date_start");
        if (this.state.lokasi_id) {
            domain.push(["lokasi_pemeriksaan", "=", parseInt(this.state.lokasi_id)]);
        }
        if (this.state.searchPenanganan) {
            domain.push("|", "|", "|", ["name", "ilike", this.state.searchPenanganan], ["owner_id.name", "ilike", this.state.searchPenanganan], ["pet_id.name", "ilike", this.state.searchPenanganan], ["doctor_id.name", "ilike", this.state.searchPenanganan]);
        }
        if (this.state.filterPenangananStatus) {
            domain.push(["state", "=", this.state.filterPenangananStatus]);
        }
        return domain;
    }

    onSearchPenanganan(ev) {
        this.state.searchPenanganan = ev.target.value;
        if (this.searchPenangananTimeout) clearTimeout(this.searchPenangananTimeout);
        this.searchPenangananTimeout = setTimeout(() => {
            this.state.penangananPage = 0;
            this._fetchPenangananData();
        }, 300);
    }

    async onFilterPenangananStatus(ev) {
        this.state.filterPenangananStatus = ev.target.value;
        this.state.penangananPage = 0;
        await this._fetchPenangananData();
    }

    async _fetchPenangananData() {
        const domain = this._getPenangananDomain();
        this.state.penangananTotal = await this.orm.searchCount("pet_clinic.visitation", domain);
        const penanganan = await this.orm.searchRead(
            "pet_clinic.visitation",
            domain,
            ["name", "owner_id", "pet_id", "doctor_id", "penanganan", "state", "lokasi_pemeriksaan", "date_start"],
            { limit: PER_PAGE, offset: this.state.penangananPage * PER_PAGE, order: "date_start desc" }
        );
        this.state.penangananData = penanganan;
    }

    async penangananNext() {
        this.state.penangananPage++;
        await this._fetchPenangananData();
    }

    async penangananPrev() {
        if (this.state.penangananPage > 0) {
            this.state.penangananPage--;
            await this._fetchPenangananData();
        }
    }

    showAllPenanganan() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Semua Penanganan",
            res_model: "pet_clinic.visitation",
            view_mode: "list,form",
            views: [[false, "list"], [false, "form"]],
            domain: this._getPenangananDomain(),
            context: {},
        });
    }

    // ─── Kunjungan Hari Ini ───────────────────────────────────────────────────
    _getVisitationTodayDomain() {
        const today = this._getToday();
        const domain = [
            ["date_start", ">=", today + " 00:00:00"],
            ["date_start", "<=", today + " 23:59:59"],
        ];
        if (this.state.lokasi_id) {
            domain.push(["lokasi_pemeriksaan", "=", parseInt(this.state.lokasi_id)]);
        }
        if (this.state.searchVisitation) {
            domain.push("|", "|", "|", ["name", "ilike", this.state.searchVisitation], ["owner_id.name", "ilike", this.state.searchVisitation], ["pet_id.name", "ilike", this.state.searchVisitation], ["doctor_id.name", "ilike", this.state.searchVisitation]);
        }
        return domain;
    }

    onSearchVisitation(ev) {
        this.state.searchVisitation = ev.target.value;
        if (this.searchVisitationTimeout) clearTimeout(this.searchVisitationTimeout);
        this.searchVisitationTimeout = setTimeout(() => {
            this.state.visitationPage = 0;
            this._fetchTodayVisitations();
        }, 300);
    }

    async _fetchTodayVisitations() {
        const domain = this._getVisitationTodayDomain();
        this.state.visitationTotal = await this.orm.searchCount("pet_clinic.visitation", domain);
        const visitations = await this.orm.searchRead(
            "pet_clinic.visitation",
            domain,
            ["name", "owner_id", "pet_id", "doctor_id", "lokasi_pemeriksaan", "date_start"],
            { limit: PER_PAGE, offset: this.state.visitationPage * PER_PAGE }
        );
        this.state.visitationsToday = visitations;
    }

    async visitationNext() {
        this.state.visitationPage++;
        await this._fetchTodayVisitations();
    }

    async visitationPrev() {
        if (this.state.visitationPage > 0) {
            this.state.visitationPage--;
            await this._fetchTodayVisitations();
        }
    }

    showAllVisitation() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Semua Kunjungan",
            res_model: "pet_clinic.visitation",
            view_mode: "list,form",
            views: [[false, "list"], [false, "form"]],
            domain: this._buildVisitationDomain(),
            context: {},
        });
    }

    // ─── Janji Hari Ini ───────────────────────────────────────────────────────
    _getAppointmentTodayDomain() {
        const today = this._getToday();
        const domain = [
            ["date", ">=", today + " 00:00:00"],
            ["date", "<=", today + " 23:59:59"],
        ];
        if (this.state.lokasi_id) {
            domain.push(["location_id", "=", parseInt(this.state.lokasi_id)]);
        }
        if (this.state.searchAppointment) {
            domain.push("|", "|", "|", ["name", "ilike", this.state.searchAppointment], ["owner_id.name", "ilike", this.state.searchAppointment], ["pet_id.name", "ilike", this.state.searchAppointment], ["doctor_id.name", "ilike", this.state.searchAppointment]);
        }
        return domain;
    }

    onSearchAppointment(ev) {
        this.state.searchAppointment = ev.target.value;
        if (this.searchAppointmentTimeout) clearTimeout(this.searchAppointmentTimeout);
        this.searchAppointmentTimeout = setTimeout(() => {
            this.state.appointmentPage = 0;
            this._fetchTodayAppointments();
        }, 300);
    }

    async _fetchTodayAppointments() {
        const domain = this._getAppointmentTodayDomain();
        this.state.appointmentTotal = await this.orm.searchCount("pet_clinic.appointment", domain);
        const appointments = await this.orm.searchRead(
            "pet_clinic.appointment",
            domain,
            ["name", "owner_id", "pet_id", "doctor_id", "groomer_id", "location_id", "date"],
            { limit: PER_PAGE, offset: this.state.appointmentPage * PER_PAGE }
        );
        this.state.appointmentsToday = appointments;
    }

    async appointmentNext() {
        this.state.appointmentPage++;
        await this._fetchTodayAppointments();
    }

    async appointmentPrev() {
        if (this.state.appointmentPage > 0) {
            this.state.appointmentPage--;
            await this._fetchTodayAppointments();
        }
    }

    showAllAppointment() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Semua Janji Temu",
            res_model: "pet_clinic.appointment",
            view_mode: "list,form",
            views: [[false, "list"], [false, "form"]],
            domain: this._getAppointmentTodayDomain(),
            context: {},
        });
    }

    // ─── Notif ────────────────────────────────────────────────────────────────
    async _fetchNotifData() {
        const today = this._getToday();
        const visitDomain = [
            ["date_start", ">=", today + " 00:00:00"],
            ["date_start", "<=", today + " 23:59:59"],
        ];
        if (this.state.lokasi_id) {
            visitDomain.push(["lokasi_pemeriksaan", "=", parseInt(this.state.lokasi_id)]);
        }
        const visitCount = await this.orm.searchCount("pet_clinic.visitation", visitDomain);
        const reminderCount = await this.orm.searchCount("pet_clinic.notif_reminder", []);
        const memberDomain = [["active", "=", true]];
        if (this.state.lokasi_id) {
            memberDomain.push(["pet_ids.visitation_ids.lokasi_pemeriksaan", "=", parseInt(this.state.lokasi_id)]);
        }
        const memberCount = await this.orm.searchCount("pet_clinic.client", memberDomain);
        this.state.notifData = [
            { name: "Notif Kunjungan", count: visitCount },
            { name: "Notif Reminder", count: reminderCount },
            { name: "Notif Member", count: memberCount },
        ];
    }

    // ─── Date Domain Helpers ──────────────────────────────────────────────────
    _getDateDomain(filter) {
        return this._getDateDomainForField(filter, "create_date");
    }

    _getDateDomainForField(filter, field) {
        let dateFrom;
        if (filter === "today") {
            dateFrom = this._getToday();
            return [
                [field, ">=", dateFrom + " 00:00:00"],
                [field, "<=", dateFrom + " 23:59:59"],
            ];
        } else if (filter === "month") {
            const d = new Date();
            d.setDate(1);
            dateFrom = d.toISOString().split("T")[0];
            return [
                [field, ">=", dateFrom + " 00:00:00"],
                [field, "<=", this._getToday() + " 23:59:59"],
            ];
        } else {
            const d = new Date();
            d.setMonth(0, 1);
            dateFrom = d.toISOString().split("T")[0];
            return [
                [field, ">=", dateFrom + " 00:00:00"],
                [field, "<=", this._getToday() + " 23:59:59"],
            ];
        }
    }

    // ─── Event Handlers ───────────────────────────────────────────────────────
    onLokasiChange(ev) {
        this.state.lokasi_id = ev.target.value || false;
    }

    onDateFromChange(ev) {
        this.state.date_from = ev.target.value;
    }

    onDateToChange(ev) {
        this.state.date_to = ev.target.value;
    }

    async onProcessClick() {
        await this._fetchDashboardData();
    }

    async onServiceFilterChange(filter) {
        this.state.serviceFilter = filter;
        this.state.servicePage = 0;
        await this._fetchServiceData();
    }

    async onPenangananFilterChange(filter) {
        this.state.penangananFilter = filter;
        this.state.penangananPage = 0;
        await this._fetchPenangananData();
    }

    // ─── KPI Domain Builders ──────────────────────────────────────────────────
    _buildVisitationDomain() {
        const domain = [];
        if (this.state.lokasi_id) {
            domain.push(["lokasi_pemeriksaan", "=", parseInt(this.state.lokasi_id)]);
        }
        if (this.state.date_from) {
            domain.push(["date_start", ">=", this.state.date_from + " 00:00:00"]);
        }
        if (this.state.date_to) {
            domain.push(["date_start", "<=", this.state.date_to + " 23:59:59"]);
        }
        return domain;
    }

    _buildMemberDomain() {
        const domain = [["active", "=", true]];
        if (this.state.lokasi_id) {
            domain.push(["pet_ids.visitation_ids.lokasi_pemeriksaan", "=", parseInt(this.state.lokasi_id)]);
        }
        return domain;
    }

    _buildPetDomain() {
        const domain = [["active", "=", true]];
        if (this.state.lokasi_id) {
            domain.push(["visitation_ids.lokasi_pemeriksaan", "=", parseInt(this.state.lokasi_id)]);
        }
        return domain;
    }

    _buildDoctorDomain() {
        const domain = [["active", "=", true]];
        if (this.state.lokasi_id) {
            domain.push(["lokasi_ids", "in", [parseInt(this.state.lokasi_id)]]);
        }
        return domain;
    }

    // ─── KPI Card Navigation ──────────────────────────────────────────────────
    openVisitations() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Kunjungan",
            res_model: "pet_clinic.visitation",
            view_mode: "list,form",
            views: [[false, "list"], [false, "form"]],
            domain: this._buildVisitationDomain(),
            context: {},
        });
    }

    openMembers() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Member",
            res_model: "pet_clinic.client",
            view_mode: "list,form",
            views: [[false, "list"], [false, "form"]],
            domain: this._buildMemberDomain(),
            context: {},
        });
    }

    openPets() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Hewan",
            res_model: "pet_clinic.pet",
            view_mode: "list,form",
            views: [[false, "list"], [false, "form"]],
            domain: this._buildPetDomain(),
            context: {},
        });
    }

    openDoctors() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Dokter",
            res_model: "pet_clinic.doctor",
            view_mode: "list,form",
            views: [[false, "list"], [false, "form"]],
            domain: this._buildDoctorDomain(),
            context: {},
        });
    }

    // ─── Table Row Click ──────────────────────────────────────────────────────
    openVisitationDetail(visitationId) {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Detail Kunjungan",
            res_model: "pet_clinic.visitation",
            view_mode: "form",
            views: [[false, "form"]],
            res_id: visitationId,
        });
    }

    openAppointmentDetail(appointmentId) {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Detail Janji Temu",
            res_model: "pet_clinic.appointment",
            view_mode: "form",
            views: [[false, "form"]],
            res_id: appointmentId,
        });
    }

    openServiceDetail(serviceId) {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Detail Layanan",
            res_model: "pet_clinic.service",
            view_mode: "form",
            views: [[false, "form"]],
            res_id: serviceId,
        });
    }

    openPenangananDetail(penanganan, state) {
        const domain = [];
        if (penanganan && penanganan !== "-") {
            domain.push(["penanganan", "=", penanganan]);
        }
        if (state && state !== "-") {
            domain.push(["state", "=", state]);
        }
        if (this.state.lokasi_id) {
            domain.push(["lokasi_pemeriksaan", "=", parseInt(this.state.lokasi_id)]);
        }
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Detail Penanganan",
            res_model: "pet_clinic.visitation",
            view_mode: "list,form",
            views: [[false, "list"], [false, "form"]],
            domain: domain,
            context: {},
        });
    }

    // ─── Product Management ───────────────────────────────────────────────────
    async _fetchProductData() {
        const domain = [["active", "=", true]];
        if (this.state.searchProduct) {
            domain.push("|", ["name", "ilike", this.state.searchProduct], ["categ_id.name", "ilike", this.state.searchProduct]);
        }
        if (this.state.filterProductType) {
            domain.push(["type", "=", this.state.filterProductType]);
        }

        this.state.productTotal = await this.orm.searchCount("product.product", domain);
        const products = await this.orm.searchRead(
            "product.product",
            domain,
            ["id", "name", "categ_id", "type", "list_price", "qty_available"],
            { limit: PER_PAGE, offset: this.state.productPage * PER_PAGE, order: "name asc" }
        );

        // Hitung usage dan omset per produk dari pet_clinic.service dalam periode
        if (products.length > 0) {
            const productIds = products.map(p => p.id);
            const periodDomain = this._getDateDomainForField(this.state.productPeriod, "date_handling");
            periodDomain.push(["service_type", "in", productIds]);
            if (this.state.lokasi_id) {
                periodDomain.push(["visitation_lokasi_id", "=", parseInt(this.state.lokasi_id)]);
            }
            const serviceRecords = await this.orm.searchRead(
                "pet_clinic.service",
                periodDomain,
                ["service_type"]
            );
            const usageMap = {};
            for (const s of serviceRecords) {
                if (s.service_type) {
                    const pid = s.service_type[0];
                    usageMap[pid] = (usageMap[pid] || 0) + 1;
                }
            }
            for (const p of products) {
                p.usage_count = usageMap[p.id] || 0;
                p.total_omset = p.usage_count * p.list_price;
            }
        }
        this.state.productData = products;

        // Summary stats
        const [totalActive, lowStockCount] = await Promise.all([
            this.orm.searchCount("product.product", [["active", "=", true]]),
            this.orm.searchCount("product.product", [["active", "=", true], ["qty_available", "<", 5], ["type", "!=", "service"]]),
        ]);

        // Cari produk terlaris dalam periode
        const allPeriodDomain = this._getDateDomainForField(this.state.productPeriod, "date_handling");
        if (this.state.lokasi_id) {
            allPeriodDomain.push(["visitation_lokasi_id", "=", parseInt(this.state.lokasi_id)]);
        }
        const allServices = await this.orm.searchRead(
            "pet_clinic.service",
            allPeriodDomain,
            ["service_type"]
        );
        const allUsageMap = {};
        for (const s of allServices) {
            if (s.service_type) {
                const pid = s.service_type[0];
                const name = s.service_type[1];
                if (!allUsageMap[pid]) allUsageMap[pid] = { count: 0, name };
                allUsageMap[pid].count++;
            }
        }
        let topProduct = "-";
        let topProductCount = 0;
        for (const data of Object.values(allUsageMap)) {
            if (data.count > topProductCount) {
                topProductCount = data.count;
                topProduct = data.name;
            }
        }
        this.state.productSummary = { totalActive, lowStockCount, topProduct, topProductCount };
    }

    onSearchProduct(ev) {
        this.state.searchProduct = ev.target.value;
        if (this.searchProductTimeout) clearTimeout(this.searchProductTimeout);
        this.searchProductTimeout = setTimeout(() => {
            this.state.productPage = 0;
            this._fetchProductData();
        }, 300);
    }

    async onFilterProductType(ev) {
        this.state.filterProductType = ev.target.value;
        this.state.productPage = 0;
        await this._fetchProductData();
    }

    async onProductPeriodChange(period) {
        this.state.productPeriod = period;
        this.state.productPage = 0;
        await this._fetchProductData();
    }

    async productNext() {
        this.state.productPage++;
        await this._fetchProductData();
    }

    async productPrev() {
        if (this.state.productPage > 0) {
            this.state.productPage--;
            await this._fetchProductData();
        }
    }

    showAllProducts() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Semua Produk",
            res_model: "product.product",
            view_mode: "list,form",
            views: [[false, "list"], [false, "form"]],
            domain: [["active", "=", true]],
            context: {},
        });
    }

    openProductDetail(productId) {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Detail Produk",
            res_model: "product.product",
            view_mode: "form",
            views: [[false, "form"]],
            res_id: productId,
        });
    }
}

registry.category("actions").add("pet_clinic_dashboard", PetClinicDashboard);

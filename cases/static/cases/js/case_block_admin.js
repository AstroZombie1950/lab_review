/* Управление видимостью секций блока и автопорядком */
(function () {
	'use strict';

	var PREFIX = 'block-section-';

	// Все известные типы
	var ALL_TYPES = [
		'intro', 'task_resume', 'tasks_grid',
		'content_full', 'content_two',
		'metrics', 'team', 'cta'
	];

	// Показать только секции для выбранного типа, остальные скрыть
	function applyType(inlineDiv, type) {
		ALL_TYPES.forEach(function (t) {
			var sections = inlineDiv.querySelectorAll('.' + PREFIX + t);
			sections.forEach(function (el) {
				el.style.display = (t === type) ? '' : 'none';
			});
		});
	}

	// Следующий порядковый номер — максимум среди существующих + 1
	function nextOrder(currentInline) {
		var max = -1;
		document.querySelectorAll('.inline-related').forEach(function (il) {
			if (il === currentInline) return;
			var inp = il.querySelector('input[id$="-order"]');
			if (!inp) return;
			var v = parseInt(inp.value, 10);
			if (!isNaN(v) && v > max) max = v;
		});
		return max + 1;
	}

	// Инициализация одного инлайна
	function initInline(div) {
		var select = div.querySelector('select[id$="-block_type"]');
		if (!select) return;

		// Показать правильные секции сразу
		applyType(div, select.value);

		// Перерисовывать при смене типа
		select.addEventListener('change', function () {
			applyType(div, this.value);
		});
	}

	// Следим за добавлением новых инлайнов через «Добавить ещё один»
	function observeInlines() {
		var observer = new MutationObserver(function (mutations) {
			mutations.forEach(function (m) {
				m.addedNodes.forEach(function (node) {
					if (node.nodeType !== 1) return;

					if (node.classList && node.classList.contains('inline-related')) {
						initInline(node);

						// Автопорядок — подставить следующий номер
						var orderInp = node.querySelector('input[id$="-order"]');
						if (orderInp && (orderInp.value === '0' || orderInp.value === '')) {
							orderInp.value = nextOrder(node);
						}
					}

					// На случай если узел вложен
					if (node.querySelectorAll) {
						node.querySelectorAll('.inline-related').forEach(initInline);
					}
				});
			});
		});

		observer.observe(document.body, { childList: true, subtree: true });
	}

	function init() {
		document.querySelectorAll('.inline-related').forEach(initInline);
		observeInlines();
	}

	if (document.readyState === 'loading') {
		document.addEventListener('DOMContentLoaded', init);
	} else {
		init();
	}
})();
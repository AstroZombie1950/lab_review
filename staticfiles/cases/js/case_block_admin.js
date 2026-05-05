/* Управление видимостью секций блока и автопорядком */
(function () {
	'use strict';

	var PREFIX = 'block-section-';

	var ALL_TYPES = [
		'intro', 'task_resume', 'tasks_grid',
		'content_full', 'content_two',
		'metrics', 'team', 'cta'
	];

	/* Показать только секции для выбранного типа, остальные скрыть */
	function applyType(inlineDiv, type) {
		ALL_TYPES.forEach(function (t) {
			var sections = inlineDiv.querySelectorAll('.' + PREFIX + t);
			sections.forEach(function (el) {
				el.style.display = (t === type) ? '' : 'none';
			});
		});
	}

	/* Следующий порядковый номер */
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

	/* Обновить бейдж видимости в заголовке */
	function updateVisibilityBadge(inlineDiv) {
		var checkbox = inlineDiv.querySelector('input[id$="-is_visible"]');
		var heading = inlineDiv.querySelector('h3');
		if (!heading || !checkbox) return;

		var old = heading.querySelector('.cb-visibility-badge');
		if (old) old.remove();

		var badge = document.createElement('span');
		badge.className = 'cb-visibility-badge ' + (checkbox.checked ? 'is-visible' : 'is-hidden');
		badge.textContent = checkbox.checked ? '✓ Показан' : '✗ Скрыт';
		heading.appendChild(badge);
	}

	/* Свернуть / развернуть — скрываем только прямой fieldset.module */
	function toggleInline(inlineDiv, collapsed) {
		/* Прямой дочерний fieldset — тело инлайна */
		var module = inlineDiv.querySelector(':scope > fieldset.module');
		if (!module) return;

		module.style.display = collapsed ? 'none' : '';

		var btn = inlineDiv.querySelector('.cb-toggle-btn');
		if (btn) btn.textContent = collapsed ? '▶' : '▼';

		inlineDiv.dataset.cbCollapsed = collapsed ? '1' : '0';
	}

	/* Добавить кнопку сворачивания в заголовок h3 */
	function addToggleButton(inlineDiv) {
		var heading = inlineDiv.querySelector('h3');
		if (!heading || heading.querySelector('.cb-toggle-btn')) return;

		var btn = document.createElement('span');
		btn.className = 'cb-toggle-btn';
		btn.textContent = '▶';
		heading.insertBefore(btn, heading.firstChild);

		/* По умолчанию свёрнут */
		toggleInline(inlineDiv, true);

		heading.style.cursor = 'pointer';
		heading.addEventListener('click', function (e) {
			if (e.target.type === 'checkbox') return;
			var isCollapsed = inlineDiv.dataset.cbCollapsed === '1';
			toggleInline(inlineDiv, !isCollapsed);
		});
	}

	/* Инициализация одного инлайна */
	function initInline(div) {
		var select = div.querySelector('select[id$="-block_type"]');
		if (!select) return;

		/* Применить тип */
		applyType(div, select.value);
		select.addEventListener('change', function () {
			applyType(div, this.value);
		});

		/* Бейдж */
		updateVisibilityBadge(div);
		var checkbox = div.querySelector('input[id$="-is_visible"]');
		if (checkbox) {
			checkbox.addEventListener('change', function () {
				updateVisibilityBadge(div);
			});
		}

		/* Сворачивание */
		addToggleButton(div);
	}

	/* Следим за добавлением новых инлайнов */
	function observeInlines() {
		var observer = new MutationObserver(function (mutations) {
			mutations.forEach(function (m) {
				m.addedNodes.forEach(function (node) {
					if (node.nodeType !== 1) return;

					if (node.classList && node.classList.contains('inline-related')) {
						initInline(node);

						var orderInp = node.querySelector('input[id$="-order"]');
						if (orderInp && (orderInp.value === '0' || orderInp.value === '')) {
							orderInp.value = nextOrder(node);
						}
					}

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
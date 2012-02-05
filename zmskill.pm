use BarnOwl::Hooks;
use strict;

package BarnOwl::Module::zmskill;

sub killzms {
    my $zmspid = BarnOwl::getvar("zmspid");
    if ($zmspid) {
        kill 9, $zmspid;
    }
}

$BarnOwl::Hooks::shutdown->add(\&killzms);
1;
